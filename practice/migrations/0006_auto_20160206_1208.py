# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0005_auto_20160206_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsskillmodel',
            name='programming',
            field=models.DecimalField(verbose_name='General skill', decimal_places=3, max_digits=4),
        ),
    ]
