from django.db import models
from django.contrib.auth.models import User
from lms.envs.common import STATE_CHOICES
from django_countries.fields import CountryField
from lms.djangoapps.ccx.models import CustomCourseForEdX


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
    def courses(self):
        return CustomCourseForEdX.objects.filter(coach__in=self.members.all())



class AffiliateMembership(models.Model):
    role_choices = (
        ('ccx_coach', 'Facilitator'),
        ('instructor', 'Course Manager'),
        ('staff', 'Program Director'),
    )

    member = models.ForeignKey(User)
    affiliate = models.ForeignKey(AffiliateEntity)
    role = models.CharField(choices=role_choices, max_length=255)
