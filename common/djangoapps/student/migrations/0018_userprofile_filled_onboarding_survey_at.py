# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0017_userprofile_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='filled_onboarding_survey_at',
            field=models.DateTimeField(default=None, null=True, blank=True),
        ),
    ]
