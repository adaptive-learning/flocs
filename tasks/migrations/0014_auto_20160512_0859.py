# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0013_auto_20160510_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmodel',
            name='toolbox',
            field=models.ForeignKey(default=None, help_text='minimal toolbox required to solve this task', null=True, to='blocks.Toolbox'),
        ),
    ]
