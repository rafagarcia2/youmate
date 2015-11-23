# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20151102_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(related_name='mates_from', to='core.Profile')),
                ('to_user', models.ForeignKey(related_name='mates_to', to='core.Profile')),
            ],
            options={
                'verbose_name': 'Mate',
                'verbose_name_plural': 'Mates',
            },
        ),
    ]
