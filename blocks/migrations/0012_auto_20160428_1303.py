# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0011_auto_20160428_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toolbox',
            name='credits',
            field=models.SmallIntegerField(help_text='total credit value of the toolbox', default=0),
        ),
    ]
