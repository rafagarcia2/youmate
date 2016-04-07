# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0005_answer_poll'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answerrate',
            name='poll',
        ),
        migrations.AddField(
            model_name='answerrate',
            name='answer',
            field=models.ForeignKey(related_name='answer_rates', default=None, to='poll.Answer'),
            preserve_default=False,
        ),
    ]
