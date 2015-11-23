# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0004_reference_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='rating',
            field=models.PositiveSmallIntegerField(default=1, choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'6')]),
        ),
    ]
