# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0010_auto_20160213_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='practicesession',
            name='task_counter',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
