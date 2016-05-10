# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_auto_20160510_0532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmodel',
            name='maze_settings',
            field=models.TextField(verbose_name='maze settings (in JSON)', default='{}'),
        ),
        migrations.AlterField(
            model_name='taskmodel',
            name='workspace_settings',
            field=models.TextField(verbose_name='workspace settings (in JSON)', default='{}'),
        ),
    ]
