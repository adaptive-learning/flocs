# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20160205_1507'),
        ('practice', '0014_auto_20160222_0530'),
    ]

    operations = [
        migrations.AddField(
            model_name='practicesession',
            name='last_task',
            field=models.ForeignKey(null=True, to='tasks.TaskModel'),
        ),
    ]
