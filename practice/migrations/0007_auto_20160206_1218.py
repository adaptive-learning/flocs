# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import practice.models.student


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0006_auto_20160206_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsskillmodel',
            name='programming',
            field=models.DecimalField(max_digits=4, verbose_name='General skill', decimal_places=3, default=practice.models.student.calculate_initial_skill),
        ),
    ]
