# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('practice', '0008_taskinstancemodel_time_end'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentTaskInfoModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_solved_instance', models.ForeignKey(to='practice.TaskInstanceModel')),
                ('student', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(to='tasks.TaskModel')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='studenttaskinfomodel',
            unique_together=set([('student', 'task')]),
        ),
        migrations.AlterIndexTogether(
            name='studenttaskinfomodel',
            index_together=set([('student', 'task')]),
        ),
    ]
