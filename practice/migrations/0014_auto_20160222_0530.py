# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0013_auto_20160218_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskinstancemodel',
            name='predicted_flow',
            field=models.FloatField(null=True, default=None),
        ),
    ]
