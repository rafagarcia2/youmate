# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160317_2233'),
        ('poll', '0003_pollrate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('text', models.TextField(max_length=400, null=True, verbose_name='Text', blank=True)),
                ('author', models.ForeignKey(related_name='answers', to='core.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.CharField(default=b'L', max_length=2, verbose_name='Rate', choices=[(b'L', 'Like'), (b'D', 'Deslike')])),
                ('created_by', models.ForeignKey(related_name='answer_rates', to='core.Profile')),
            ],
            options={
                'verbose_name': 'Answer Rate',
                'verbose_name_plural': 'Answer Rates',
            },
        ),
        migrations.RemoveField(
            model_name='pollrate',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='pollrate',
            name='poll',
        ),
        migrations.AlterField(
            model_name='poll',
            name='author',
            field=models.ForeignKey(related_name='polls', to='core.Profile'),
        ),
        migrations.DeleteModel(
            name='PollRate',
        ),
        migrations.AddField(
            model_name='answerrate',
            name='poll',
            field=models.ForeignKey(related_name='answer_rates', to='poll.Poll'),
        ),
    ]
