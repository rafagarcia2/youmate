# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('text', models.TextField(max_length=400, null=True, verbose_name=b'Texto da referencia', blank=True)),
                ('active', models.BooleanField(default=False)),
                ('rating', models.PositiveSmallIntegerField(default=1, choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5')])),
                ('from_user', models.ForeignKey(related_name='references_from', to='core.Profile')),
                ('to_user', models.ForeignKey(related_name='references_to', to='core.Profile')),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': 'Reference',
                'verbose_name_plural': 'References',
            },
        ),
    ]
