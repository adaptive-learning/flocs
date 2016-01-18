# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0002_auto_20160108_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructionsmodel',
            name='text_cs',
            field=models.CharField(null=True, max_length=255, verbose_name='Text of instruction shown in game page'),
        ),
        migrations.AddField(
            model_name='instructionsmodel',
            name='text_en',
            field=models.CharField(null=True, max_length=255, verbose_name='Text of instruction shown in game page'),
        ),
    ]
