# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0012_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='free_credits',
            field=models.IntegerField(verbose_name='number of free credits to spend', default=0),
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='total_credits',
            field=models.IntegerField(verbose_name='total number of credits earned', default=0),
        ),
    ]
