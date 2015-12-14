# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_profile_languages'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Status', choices=[(b'L', 'Local'), (b'T', 'Traveler')]),
        ),
    ]
