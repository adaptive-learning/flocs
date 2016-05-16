# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0004_auto_20160501_0310'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instruction',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='instruction',
            name='order',
            field=models.SmallIntegerField(default=0, help_text='instructions with lower "order" will be shown first'),
        ),
    ]
