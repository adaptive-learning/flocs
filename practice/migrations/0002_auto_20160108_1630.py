# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskinstancemodel',
            name='reported_flow',
            field=models.SmallIntegerField(choices=[(0, 'unknown'), (1, 'very difficult'), (2, 'difficult'), (3, 'just right'), (4, 'easy')], default=0),
        ),
    ]
