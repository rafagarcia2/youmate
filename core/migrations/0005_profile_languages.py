# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0001_initial'),
        ('core', '0004_profile_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='languages',
            field=models.ManyToManyField(related_name='profiles', to='language.Language'),
        ),
    ]
