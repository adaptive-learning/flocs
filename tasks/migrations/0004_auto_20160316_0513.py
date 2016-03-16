# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_taskmodel_required_blocks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskmodel',
            name='required_blocks',
        ),
        migrations.AddField(
            model_name='taskmodel',
            name='block_level',
            field=models.PositiveSmallIntegerField(default=0, help_text='the most difficult block the task requires'),
        ),
    ]
