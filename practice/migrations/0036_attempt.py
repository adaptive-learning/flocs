# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0035_taskinstancemodel_blocks'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('time', models.DateTimeField(help_text='time when the attempt was logged', default=datetime.datetime.now)),
                ('success', models.BooleanField(help_text='whether the task was solved by this attempt or not', default=False)),
                ('order', models.IntegerField(help_text='order of the attempt within this task instance', default=0)),
                ('code', models.TextField(help_text="XML representation of student's code")),
                ('task_instance', models.ForeignKey(to='practice.TaskInstanceModel', help_text='task instance being solved')),
            ],
        ),
    ]
