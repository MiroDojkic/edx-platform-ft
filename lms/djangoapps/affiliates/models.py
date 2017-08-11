from django.db import models, IntegrityError, transaction
from django.db.models import Q, F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
from lms.envs.common import STATE_CHOICES
from django_countries.fields import CountryField
from lms.djangoapps.ccx.models import CustomCourseForEdX
from instructor.access import allow_access, revoke_access
from ccx_keys.locator import CCXLocator
from courseware.courses import get_course_by_id
from contextlib import contextmanager
from courseware.courses import get_course_with_access, get_course_by_id
from opaque_keys.edx.keys import CourseKey
from student.models import CourseAccessRole
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from lms.djangoapps.instructor.enrollment import enroll_email


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.id, filename)


class AffiliateEntity(models.Model):
    slug = models.SlugField(max_length=255, unique=True, default='')

    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(null=True, blank=True, max_length=255, default='')
    phone_number = models.CharField(null=True, blank=True, max_length=255, default='')
    address = models.CharField(null=True, blank=True, max_length=255, default='')
    city = models.CharField(null=True, blank=True, max_length=255, default='')
    zipcode = models.CharField(null=True, blank=True, max_length=255, default='')
    website = models.CharField(null=True, blank=True, max_length=255, default='')
    facebook = models.CharField(null=True, blank=True, max_length=255, default='')
    twitter = models.CharField(null=True, blank=True, max_length=255, default='')
    linkedin = models.CharField(null=True, blank=True, max_length=255, default='')
    state = models.CharField(null=True, blank=True, default='na', choices=STATE_CHOICES, max_length=255)
    country = CountryField(blank=True, null=True)

    geoposition_x = models.IntegerField(null=True, blank=True)
    geoposition_y = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    members = models.ManyToManyField(User, through='AffiliateMembership')

    def save(self, *args, **kwargs):
        slug = slugify(self.name)

        slug_exists = AffiliateEntity.objects.filter(slug=slug).exclude(pk=self.pk).exists()

        if slug_exists:
            self.slug = '-'.join([slug, get_random_string(4)])
        else:
            self.slug = slug

        super(AffiliateEntity, self).save(*args, **kwargs)


    def delete(self):
        with transaction.atomic():
            self.courses.delete()
            super(AffiliateEntity, self).delete()

    class Meta:
        unique_together = ('email', 'name')

    def __unicode__(self):
        return self.name

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return 'https://s3.amazonaws.com/fasttrac-beta/default_full.png'

    @property
    def memberships(self):
        return AffiliateMembership.objects.filter(affiliate=self)

    @property
    def courses(self):
        return CustomCourseForEdX.objects.filter(coach__in=self.members.all())



class AffiliateMembership(models.Model):
    role_choices = (
        ('ccx_coach', 'Facilitator'),
        ('instructor', 'Course Manager'),
        ('staff', 'Program Director'),
    )

    member = models.ForeignKey(User)
    affiliate = models.ForeignKey(AffiliateEntity, on_delete=models.CASCADE)
    role = models.CharField(choices=role_choices, max_length=255)

    @classmethod
    def find_by_user(self, user):
        return self.objects.get(member=user)



@receiver(post_save, sender=AffiliateMembership, dispatch_uid="add_affiliate_course_enrollments")
def add_affiliate_course_enrollments(sender, instance, **kwargs):
    'Allow staff or instructor access to affiliate member into all affiliate courses if they are staff or instructor member.'
    if not instance.role == 'ccx_coach':
        for ccx in instance.affiliate.courses:
            ccx_locator = CCXLocator.from_course_locator(ccx.course_id, ccx.id)
            course = get_course_by_id(ccx_locator)

            try:
                with transaction.atomic():
                    allow_access(course, instance.member, instance.role, False)
            except IntegrityError:
                print 'IntegrityError: Allow access failed.'

    # Program Director and Course Manager needs to be CCX coach on FastTrac course
    course_overviews = CourseOverview.objects.exclude(id__startswith='ccx-')

    if instance.role == 'staff' or instance.role == 'instructor':
        for course_overview in course_overviews:
            course_id = course_overview.id
            course = get_course_by_id(course_id)

            try:
                with transaction.atomic():
                    allow_access(course, instance.member, 'ccx_coach', False)
            except IntegrityError:
                print 'IntegrityError: CCX coach failed.'

    elif instance.role == 'ccx_coach':
        for course_overview in course_overviews:
            course_id = course_overview.id

            enroll_email(course_id, instance.member.email, auto_enroll=True)



@receiver(post_delete, sender=AffiliateMembership, dispatch_uid="remove_affiliate_course_enrollments")
def remove_affiliate_course_enrollments(sender, instance, **kwargs):
    'Remove all privileges over all affiliate courses.'
    for ccx in instance.affiliate.courses:
        ccx_locator = CCXLocator.from_course_locator(ccx.course_id, ccx.id)
        course = get_course_by_id(ccx_locator)

        revoke_access(course, instance.member, instance.role, False)

    # Remove CCX coach on FastTrac course
    if instance.role == 'staff' or instance.role == 'instructor':
        course_overviews = CourseOverview.objects.exclude(id__startswith='ccx-')
        for course_overview in course_overviews:
            course_id = course_overview.id
            course = get_course_by_id(course_id)

            revoke_access(course, instance.member, 'ccx_coach', False)
