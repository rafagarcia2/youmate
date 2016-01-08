# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mate', '0005_auto_20160108_1828'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mate',
            unique_together=set([]),
        ),
    ]
