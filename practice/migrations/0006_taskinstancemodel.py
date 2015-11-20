# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0001_initial'),
        ('practice', '0005_auto_20151120_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskInstanceModel',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('time_start', models.DateTimeField(default=datetime.datetime.now)),
                ('time_spent', models.TimeField()),
                ('solved', models.BooleanField(default=False)),
                ('reported_flow', models.SmallIntegerField(default=0, choices=[(0, 'unknown'), (1, 'too difficult'), (2, 'just right'), (3, 'too easy')])),
                ('predicted_flow', models.FloatField()),
                ('attempts_count', models.IntegerField(default=0)),
                ('student', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(to='tasks.TaskModel')),
            ],
        ),
    ]
