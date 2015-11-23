# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mate', '0001_initial'),
        ('core', '0002_auto_20151102_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mates',
            field=models.ManyToManyField(related_name='mates_by', through='mate.Mate', to='core.Profile'),
        ),
    ]
