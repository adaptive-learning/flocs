# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockmodel',
            name='name_cs',
            field=models.TextField(null=True, verbose_name='name of a block'),
        ),
        migrations.AddField(
            model_name='blockmodel',
            name='name_en',
            field=models.TextField(null=True, verbose_name='name of a block'),
        ),
    ]
