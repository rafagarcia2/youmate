# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0004_auto_20160406_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='poll',
            field=models.ForeignKey(related_name='answers', default=None, to='poll.Poll'),
            preserve_default=False,
        ),
    ]
