# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0012_auto_20160428_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolbox',
            name='credits',
            field=models.SmallIntegerField(help_text='price to upgrade from the previous toolbox level', default=0),
        ),
    ]
