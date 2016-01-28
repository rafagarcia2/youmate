# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def delete_animais_and_amizades_interests(apps, schema_editor):
    Interest = apps.get_model('interest', 'Interest')
    Interest.objects.filter(
        image_class__in=['animais', 'amizades']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0003_auto_20151123_1920'),
    ]

    operations = [
        migrations.RunPython(delete_animais_and_amizades_interests)
    ]
