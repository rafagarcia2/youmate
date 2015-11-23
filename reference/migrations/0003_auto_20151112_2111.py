# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0002_auto_20151112_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='text',
            field=models.TextField(max_length=400, verbose_name=b'Texto da referencia'),
        ),
    ]
