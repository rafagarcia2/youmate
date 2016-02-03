# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mate', '0006_auto_20160108_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mate',
            name='status',
            field=models.CharField(default=b'P', max_length=2, choices=[(b'P', b'Pending'), (b'M', b'Mate')]),
        ),
    ]
