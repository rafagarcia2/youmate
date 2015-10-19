# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('about', models.TextField(max_length=400, null=True, verbose_name='About', blank=True)),
                ('age', models.IntegerField(null=True, verbose_name='Age', blank=True)),
                ('genre', models.CharField(default=b'X', choices=[(b'X', 'X'), (b'M', 'Men'), (b'W', 'Women')], max_length=15, blank=True, null=True, verbose_name='Genre')),
                ('job_title', models.CharField(max_length=100, null=True, verbose_name='Job title', blank=True)),
                ('education', models.CharField(max_length=100, null=True, verbose_name='Education', blank=True)),
                ('born_city', models.CharField(max_length=100, null=True, verbose_name='Born city', blank=True)),
                ('livin_city', models.CharField(max_length=100, null=True, verbose_name='Living city', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
