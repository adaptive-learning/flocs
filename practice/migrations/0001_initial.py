# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskModel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('maze_settings', models.TextField(verbose_name='Maze settings in JSON')),
                ('workspace_settings', models.TextField(verbose_name='Workspace settings in JSON')),
            ],
        ),
    ]
