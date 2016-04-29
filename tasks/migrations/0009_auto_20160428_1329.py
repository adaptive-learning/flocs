# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0012_auto_20160428_1303'),
        ('tasks', '0008_taskmodel__contained_concepts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskmodel',
            name='level',
        ),
        migrations.AddField(
            model_name='taskmodel',
            name='toolbox',
            field=models.ForeignKey(help_text='minimal toolbox requried to solve this task', default=None, to='blocks.Toolbox', null=True),
        ),
    ]
