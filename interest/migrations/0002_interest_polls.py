# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0001_initial'),
        ('interest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interest',
            name='polls',
            field=models.ManyToManyField(related_name='interests', to='poll.Poll'),
        ),
    ]
