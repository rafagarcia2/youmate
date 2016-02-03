# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20160122_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email_code',
            field=models.CharField(default=b'F7T2IWUF8EAQAQ186YXEX9TK4DESUNB5', max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone_code',
            field=models.CharField(default=b'XK0EH1', max_length=50),
        ),
    ]
