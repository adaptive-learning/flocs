# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import practice.models.student


class Migration(migrations.Migration):

    dependencies = [
        ('levels', '__first__'),
        ('practice', '0026_remove_studentmodel_available_blocks'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='level',
            field=models.ForeignKey(null=True, to='levels.Level', default=practice.models.student._get_lowest_level),
        ),
    ]
