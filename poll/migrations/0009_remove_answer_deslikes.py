# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 23:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0008_auto_20160511_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='deslikes',
        ),
    ]