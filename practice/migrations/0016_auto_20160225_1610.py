# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0015_practicesession_last_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentmodel',
            name='session',
        ),
        migrations.RemoveField(
            model_name='taskinstancemodel',
            name='session',
        ),
        migrations.AddField(
            model_name='practicesession',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='practicesession',
            name='student',
            field=models.ForeignKey(null=True, to='practice.StudentModel'),
        ),
        migrations.AlterField(
            model_name='practicesession',
            name='last_task',
            field=models.ForeignKey(null=True, to='practice.TaskInstanceModel'),
        ),
    ]
