# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0011_taskmodel__block_limit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskmodel',
            old_name='_block_limit',
            new_name='_blocks_limit',
        ),
    ]
