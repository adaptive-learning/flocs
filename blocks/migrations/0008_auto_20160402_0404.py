# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0007_auto_20160325_1227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blockmodel',
            name='difficulty',
        ),
        migrations.RemoveField(
            model_name='blockmodel',
            name='price',
        ),
        migrations.AddField(
            model_name='blockmodel',
            name='level',
            field=models.SmallIntegerField(default=1, help_text='level required to use this block'),
        ),
    ]
