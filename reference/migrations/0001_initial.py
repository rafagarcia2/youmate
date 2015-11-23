# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_profile_mates'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
                ('from_user', models.ForeignKey(related_name='references_from', to='core.Profile')),
                ('to_user', models.ForeignKey(related_name='references_to', to='core.Profile')),
            ],
            options={
                'verbose_name': 'Reference',
                'verbose_name_plural': 'References',
            },
        ),
    ]
