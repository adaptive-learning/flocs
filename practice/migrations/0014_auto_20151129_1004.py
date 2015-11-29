# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0013_auto_20151125_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructionsmodel',
            name='flow_factor',
            field=models.SmallIntegerField(unique=True, choices=[(255, 'instructions on basics of the game'), (4, 'instructions concerning logical expresions'), (5, 'instructions concerning colors'), (6, 'instructions concerning tokens'), (7, 'instructions concerning pits'), (2, 'instructions concerning loops'), (3, 'instructions on how to use conditions')], default=255, verbose_name='Factor to which these instructions belong'),
        ),
    ]
