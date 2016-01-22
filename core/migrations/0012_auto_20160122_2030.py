# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20160122_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email_code',
            field=models.CharField(default=b'GMQSEE922RUFIZXTBJE3MPP3PDOA7EOL', max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_code',
            field=models.CharField(default=b'OJWKCZ', max_length=50),
        ),
    ]
