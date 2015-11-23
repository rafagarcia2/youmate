# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0003_auto_20151112_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
