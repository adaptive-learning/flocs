# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
        ('practice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TasksDifficultyModel',
            fields=[
                ('task', models.OneToOneField(primary_key=True, serialize=False, to='tasks.TaskModel')),
                ('programming', models.DecimalField(decimal_places=3, verbose_name='General difficulty of the task', max_digits=4)),
                ('conditions', models.BooleanField(verbose_name='Diffuculty of the conditions concept in the task')),
                ('loops', models.BooleanField(verbose_name='Diffuculty of the loops concept in the task')),
                ('logic_expr', models.BooleanField(verbose_name='Diffuculty of the logic expressions concept in the task')),
                ('colors', models.BooleanField(verbose_name='Diffuculty of the colors concept in the task')),
                ('tokens', models.BooleanField(verbose_name='Diffuculty of the tokens concept in the task')),
                ('pits', models.BooleanField(verbose_name='Diffuculty of the pits concept in the task')),
            ],
        ),
    ]
