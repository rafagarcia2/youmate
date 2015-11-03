# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchQuery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('living_city', models.CharField(max_length=100, null=True, verbose_name='Living city', blank=True)),
                ('start', models.DateField(null=True, verbose_name='Start', blank=True)),
                ('end', models.DateField(null=True, verbose_name='End', blank=True)),
                ('count', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name': 'Search',
                'verbose_name_plural': 'Searchs',
            },
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='livin_city',
            new_name='living_city',
        ),
        migrations.AddField(
            model_name='searchquery',
            name='profile',
            field=models.ForeignKey(to='core.Profile'),
        ),
        migrations.AlterUniqueTogether(
            name='searchquery',
            unique_together=set([('living_city', 'start', 'end', 'profile')]),
        ),
    ]
