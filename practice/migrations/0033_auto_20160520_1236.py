# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0032_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskinstancemodel',
            name='reported_flow',
            field=models.SmallIntegerField(choices=[(0, 'UNKNOWN'), (1, 'VERY_DIFFICULT'), (2, 'DIFFICULT'), (3, 'RIGHT'), (4, 'EASY')], default=0),
        ),
    ]
