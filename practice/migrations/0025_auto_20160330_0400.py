# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0024_auto_20160319_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskinstancemodel',
            name='speed_bonus',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='taskinstancemodel',
            name='attempt_count',
            field=models.IntegerField(default=0, help_text='how many attempts did the student take (attempt = running a program)'),
        ),
    ]
