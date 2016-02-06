# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0004_auto_20160121_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsskillmodel',
            name='programming',
            field=models.DecimalField(default=Decimal('-0.984'), decimal_places=3, verbose_name='General skill', max_digits=4),
        ),
    ]
