# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0007_auto_20151120_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskinstancemodel',
            name='time_end',
            field=models.DateTimeField(null=True, default=None),
        ),
    ]
