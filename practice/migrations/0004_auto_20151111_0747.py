# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0003_auto_20151111_0739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='difficultymodel',
            name='task',
        ),
        migrations.DeleteModel(
            name='DifficultyModel',
        ),
    ]
