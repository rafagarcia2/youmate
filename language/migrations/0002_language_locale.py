# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='locale',
            field=models.CharField(max_length=10, null=True, verbose_name='Locale', blank=True),
        ),
    ]
