# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mate', '0003_auto_20151229_1915'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mate',
            unique_together=set([]),
        ),
    ]
