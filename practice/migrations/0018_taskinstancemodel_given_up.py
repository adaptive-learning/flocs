# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0017_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskinstancemodel',
            name='given_up',
            field=models.BooleanField(default=False),
        ),
    ]
