# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='mates',
            field=models.ManyToManyField(related_name='mates+', through='mate.Mate', to='core.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'photos/', blank=True),
        ),
    ]
