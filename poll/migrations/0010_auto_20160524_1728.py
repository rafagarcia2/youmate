# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-24 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0009_remove_answer_deslikes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='text',
            field=models.CharField(max_length=400, verbose_name='Text'),
        ),
    ]
