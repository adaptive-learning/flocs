# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_taskmodel_solution'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmodel',
            name='_block_limit',
            field=models.PositiveSmallIntegerField(help_text='Limit on number of blocks student can use, including start block', default=None, null=True),
        ),
    ]
