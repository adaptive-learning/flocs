# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DifficultyModel',
            fields=[
                ('difficulty', models.DecimalField(verbose_name='Difficulty evaluation', max_digits=4, decimal_places=3)),
                ('task', models.OneToOneField(primary_key=True, serialize=False, to='tasks.TaskModel')),
            ],
        ),
    ]
