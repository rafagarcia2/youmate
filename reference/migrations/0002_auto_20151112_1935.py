# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reference', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='text',
            field=models.TextField(verbose_name=b'Texto da referencia'),
        ),
    ]
