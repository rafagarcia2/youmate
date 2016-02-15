# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0006_auto_20160203_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='text',
            field=models.TextField(max_length=400, null=True, verbose_name=b'Texto da referencia', blank=True),
        ),
    ]
