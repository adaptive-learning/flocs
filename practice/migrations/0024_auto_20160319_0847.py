# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0023_taskinstancemodel_earned_credits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskinstancemodel',
            name='earned_credits',
            field=models.SmallIntegerField(null=True, default=0),
        ),
    ]
