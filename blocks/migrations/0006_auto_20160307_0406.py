# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0005_blockmodel_difficulty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockmodel',
            name='price',
            field=models.IntegerField(default=0, help_text='number of currency units required to buy this block'),
        ),
    ]
