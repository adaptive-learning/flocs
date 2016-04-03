# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20160316_0513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskmodel',
            name='block_level',
        ),
        migrations.AddField(
            model_name='taskmodel',
            name='level',
            field=models.SmallIntegerField(default=1),
        ),
    ]
