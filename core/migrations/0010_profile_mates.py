# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mate', '0003_auto_20151229_1915'),
        ('core', '0009_remove_profile_mates'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mates',
            field=models.ManyToManyField(related_name='mates_related_to+', through='mate.Mate', to='core.Profile'),
        ),
    ]
