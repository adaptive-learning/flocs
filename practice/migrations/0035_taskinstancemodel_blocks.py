# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0014_remove_block_level'),
        ('practice', '0034_taskinstancemodel_instructions'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskinstancemodel',
            name='blocks',
            field=models.ManyToManyField(help_text='blocks available in toolbox', to='blocks.Block'),
        ),
    ]
