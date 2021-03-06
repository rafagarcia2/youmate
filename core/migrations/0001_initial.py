# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoreUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'swappable': 'AUTH_USER_MODEL',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('about', models.TextField(max_length=400, null=True, verbose_name='About', blank=True)),
                ('age', models.IntegerField(null=True, verbose_name='Age', blank=True)),
                ('genre', models.CharField(default=b'X', choices=[(b'X', 'X'), (b'M', 'Men'), (b'W', 'Women')], max_length=15, blank=True, null=True, verbose_name='Genre')),
                ('status', models.CharField(blank=True, max_length=15, null=True, verbose_name='Status', choices=[(b'L', 'Local'), (b'T', 'Traveler')])),
                ('phone', models.CharField(max_length=40, null=True, verbose_name='Phone', blank=True)),
                ('job_title', models.CharField(max_length=100, null=True, verbose_name='Job title', blank=True)),
                ('education', models.CharField(max_length=100, null=True, verbose_name='Education', blank=True)),
                ('born_city', models.CharField(max_length=100, null=True, verbose_name='Born city', blank=True)),
                ('living_city', models.CharField(max_length=100, null=True, verbose_name='Living city', blank=True)),
                ('photo', models.ImageField(null=True, upload_to=b'photos/', blank=True)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('email_code', models.CharField(default=core.models.code_generate32, max_length=50)),
                ('is_phone_verified', models.BooleanField(default=False)),
                ('phone_code', models.CharField(default=core.models.code_generate6, max_length=50)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='SearchQuery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('living_city', models.CharField(max_length=100, null=True, verbose_name='Living city', blank=True)),
                ('start', models.DateField(null=True, verbose_name='Start', blank=True)),
                ('end', models.DateField(null=True, verbose_name='End', blank=True)),
                ('count', models.IntegerField(default=1)),
                ('profile', models.ForeignKey(to='core.Profile')),
            ],
            options={
                'verbose_name': 'Search',
                'verbose_name_plural': 'Searchs',
            },
        ),
        migrations.AlterUniqueTogether(
            name='searchquery',
            unique_together=set([('living_city', 'start', 'end', 'profile')]),
        ),
    ]
