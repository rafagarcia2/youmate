# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160317_2233'),
        ('poll', '0002_auto_20160331_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rate', models.CharField(default=b'L', max_length=2, verbose_name='Rate', choices=[(b'L', 'Like'), (b'D', 'Deslike')])),
                ('created_by', models.ForeignKey(related_name='polls_rates', to='core.Profile')),
                ('poll', models.ForeignKey(related_name='polls_rates', to='poll.Poll')),
            ],
            options={
                'verbose_name': 'Poll Rate',
                'verbose_name_plural': 'PollR ates',
            },
        ),
    ]
