# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_auto_20160428_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmodel',
            name='solution',
            field=models.TextField(default=None, help_text='XML representation of a Blockly program', null=True),
        ),
    ]
