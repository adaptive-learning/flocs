# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0022_auto_20160305_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskinstancemodel',
            name='earned_credits',
            field=models.SmallIntegerField(null=True, default=None),
        ),
    ]
