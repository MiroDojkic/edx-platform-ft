from django.db import models
from django.db.models import Q, F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from lms.envs.common import STATE_CHOICES
from django_countries.fields import CountryField
from lms.djangoapps.ccx.models import CustomCourseForEdX
from instructor.access import allow_access, revoke_access
from ccx_keys.locator import CCXLocator
from courseware.courses import get_course_by_id
from contextlib import contextmanager



def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.id, filename)


class AffiliateEntity(models.Model):
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(null=True, blank=True, max_length=255, default='')
    phone_number = models.CharField(null=True, blank=True, max_length=255, default='')
    address = models.CharField(null=True, blank=True, max_length=255, default='')
    city = models.CharField(null=True, blank=True, max_length=255, default='')
    zipcode = models.CharField(null=True, blank=True, max_length=255, default='')
    facebook = models.CharField(null=True, blank=True, max_length=255, default='')
    twitter = models.CharField(null=True, blank=True, max_length=255, default='')
    linkedin = models.CharField(null=True, blank=True, max_length=255, default='')
    state = models.CharField(null=True, blank=True, default='na', choices=STATE_CHOICES, max_length=255)
    country = CountryField(blank=True, null=True)

    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    members = models.ManyToManyField(User, through='AffiliateMembership')

    def __unicode__(self):
        return self.name

    @property
    def memberships(self):
        return AffiliateMembership.objects.filter(affiliate=self)

    @property
    def courses(self):
        return CustomCourseForEdX.objects.filter(coach__in=self.members.all(), id=F('original_ccx_id'))



class AffiliateMembership(models.Model):
    role_choices = (
        ('ccx_coach', 'Facilitator'),
        ('instructor', 'Course Manager'),
        ('staff', 'Program Director'),
    )

    member = models.ForeignKey(User)
    affiliate = models.ForeignKey(AffiliateEntity)
    role = models.CharField(choices=role_choices, max_length=255)



@contextmanager
def ccx_course(ccx_locator):
    """Create a context in which the course identified by course_locator exists
    """
    course = get_course_by_id(ccx_locator)
    yield course


@receiver(post_save, sender=AffiliateMembership, dispatch_uid="add_affiliate_course_enrollments")
def add_affiliate_course_enrollments(sender, instance, **kwargs):
    'Allow staff or instructor access to affiliate member into all affiliate courses if they are staff or instructor member.'
    if not instance.role == 'ccx_coach':
        for ccx in instance.affiliate.courses:
            ccx_locator = CCXLocator.from_course_locator(ccx.course_id, ccx.id)
            with ccx_course(ccx_locator) as course:
                allow_access(course, instance.member, instance.role, False)


@receiver(post_delete, sender=AffiliateMembership, dispatch_uid="remove_affiliate_course_enrollments")
def remove_affiliate_course_enrollments(sender, instance, **kwargs):
    'Remove all privileges over all affiliate courses.'
    for ccx in instance.affiliate.courses:
        ccx_locator = CCXLocator.from_course_locator(ccx.course_id, ccx.id)

        with ccx_course(ccx_locator) as course:
            revoke_access(course, instance.member, instance.role, False)

