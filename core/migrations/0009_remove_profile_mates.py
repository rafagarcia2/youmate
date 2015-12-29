# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20151229_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='mates',
        ),
    ]
