# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0011_auto_20151124_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructionsModel',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('flow_factor', models.SmallIntegerField(default=255, verbose_name='Factor to which these instructions belong', choices=[(255, 'instructions on basics of the game'), (4, 'instructions conserning logical expresions'), (5, 'instructions conserning colors'), (6, 'instructions conserning tokens'), (7, 'instructions conserning pits'), (2, 'instructions conserning loops'), (3, 'instructions on how to use conditions')])),
                ('text', models.CharField(verbose_name='Text of instruction shown in game page', max_length=255)),
            ],
        ),
    ]
