# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0012_instructionsmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructionsmodel',
            name='flow_factor',
            field=models.SmallIntegerField(unique=True, default=255, choices=[(255, 'instructions on basics of the game'), (4, 'instructions conserning logical expresions'), (5, 'instructions conserning colors'), (6, 'instructions conserning tokens'), (7, 'instructions conserning pits'), (2, 'instructions conserning loops'), (3, 'instructions on how to use conditions')], verbose_name='Factor to which these instructions belong'),
        ),
    ]
