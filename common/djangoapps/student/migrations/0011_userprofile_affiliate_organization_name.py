# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_auto_20170411_0752'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='affiliate_organization_name',
            field=models.CharField(default=b'', max_length=255, null=True, blank=True),
        ),
    ]
