# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0009_auto_20160419_0651'),
    ]

    operations = [
        migrations.CreateModel(
            name='Toolbox',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('level', models.SmallIntegerField(default=1, help_text='defines ordering of toolboxes (higher level = more advanced toolbox)')),
                ('name', models.CharField(max_length=50, unique=True, help_text='unique name of this toolbox')),
                ('credits', models.SmallIntegerField(default=0, help_text='credits required for update from the previous toolbox')),
                ('blocks', models.ManyToManyField(to='blocks.Block', help_text='all blocks contained in this toolbox')),
            ],
        ),
    ]
