# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_profile_mates'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email_code',
            field=models.CharField(default=core.models.code_generate32, max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_phone_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_code',
            field=models.CharField(default=core.models.code_generate6, max_length=50),
        ),
    ]
