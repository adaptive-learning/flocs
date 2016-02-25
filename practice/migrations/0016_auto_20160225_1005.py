# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0015_practicesession_last_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studenttaskinfomodel',
            name='student',
            field=models.ForeignKey(to='practice.StudentModel'),
        ),
        migrations.AlterField(
            model_name='taskinstancemodel',
            name='student',
            field=models.ForeignKey(to='practice.StudentModel'),
        ),
    ]
