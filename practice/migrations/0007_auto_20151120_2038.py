# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0006_taskinstancemodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskinstancemodel',
            old_name='attempts_count',
            new_name='attempt_count',
        ),
        migrations.AlterField(
            model_name='taskinstancemodel',
            name='time_spent',
            field=models.IntegerField(default=0),
        ),
    ]
