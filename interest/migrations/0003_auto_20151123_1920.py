# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0002_interest_image_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interest',
            old_name='image_url',
            new_name='image_class',
        ),
    ]
