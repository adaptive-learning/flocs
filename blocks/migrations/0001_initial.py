# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlockModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.TextField(verbose_name='name of a block')),
                ('identifier', models.TextField(verbose_name='unique identifier of a block used internally')),
                ('price', models.IntegerField(verbose_name='number of currency units required to buy this block')),
            ],
        ),
    ]
