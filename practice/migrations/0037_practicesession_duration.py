# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0036_attempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='practicesession',
            name='duration',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
