# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0010_auto_20151124_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studenttaskinfomodel',
            name='last_instance',
            field=models.ForeignKey(to='practice.TaskInstanceModel', null=True, default=None),
        ),
    ]
