from django.db import models
from django.contrib.auth.models import User
from lms.envs.common import STATE_CHOICES
from django_countries.fields import CountryField


class AffiliateEntity(models.Model):
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(null=True, blank=True, max_length=255)
    phone_number = models.CharField(null=True, blank=True, default='', max_length=255)
    address = models.CharField(null=True, blank=True, max_length=255)
    city = models.CharField(null=True, blank=True, max_length=255)
    zipcode = models.CharField(null=True, blank=True, max_length=255)
    facebook = models.CharField(null=True, blank=True, max_length=255)
    twitter = models.CharField(null=True, blank=True, max_length=255)
    linkedin = models.CharField(null=True, blank=True, max_length=255)
    state = models.CharField(null=True, blank=True, default='na', choices=STATE_CHOICES, max_length=255)
    country = CountryField(blank=True, null=True)


class AffiliateMembership(models.Model):
    role_choices = (
        ('ccx_coach', 'Facilitator'),
        ('instructor', 'Course Manager'),
        ('staff', 'Program Director'),
    )

    member = models.ForeignKey(User)
    affiliate = models.ForeignKey(AffiliateEntity)
    role = models.CharField(choices=STATE_CHOICES, max_length=255)
