# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mate',
            name='status',
            field=models.CharField(default=b'P', max_length=2, choices=[(b'P', b'Pending'), (b'M', b'Mate'), (b'B', b'Blocked')]),
        ),
    ]
