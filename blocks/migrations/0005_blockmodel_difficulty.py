# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0004_auto_20160305_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockmodel',
            name='difficulty',
            field=models.FloatField(default=1.0, help_text='real number between -1 (easiest) and 1 (most difficult)'),
        ),
    ]
