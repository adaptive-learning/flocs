# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0018_taskinstancemodel_given_up'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionTaskInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('order', models.PositiveSmallIntegerField()),
                ('session', models.ForeignKey(to='practice.PracticeSession', related_name='task_instances_set')),
                ('task_instance', models.ForeignKey(to='practice.TaskInstanceModel')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='sessiontaskinstance',
            unique_together=set([('session', 'order')]),
        ),
    ]
