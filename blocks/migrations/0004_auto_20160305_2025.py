# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0003_auto_20160305_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockmodel',
            name='identifiers',
            field=models.TextField(verbose_name='unique identifier(s) of a block(s) used internally'),
        ),
        migrations.AlterField(
            model_name='blockmodel',
            name='price',
            field=models.IntegerField(verbose_name='number of currency units required to buy this block', default=0),
        ),
    ]
