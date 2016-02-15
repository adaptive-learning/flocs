# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0009_auto_20160212_0441'),
    ]

    operations = [
        migrations.AddField(
            model_name='studenttaskinfomodel',
            name='last_solved_instance',
            field=models.OneToOneField(to='practice.TaskInstanceModel', default=None, related_name='+', null=True),
        ),
        migrations.AlterField(
            model_name='studenttaskinfomodel',
            name='last_instance',
            field=models.OneToOneField(to='practice.TaskInstanceModel', default=None, related_name='+', null=True),
        ),
    ]
