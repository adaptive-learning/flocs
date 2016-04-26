# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0029_auto_20160420_0234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasksdifficultymodel',
            name='task',
        ),
        migrations.DeleteModel(
            name='TasksDifficultyModel',
        ),
    ]
