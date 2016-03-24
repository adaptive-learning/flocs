# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0006_auto_20160307_0406'),
    ]

    operations = [
        migrations.AddField(
            model_name='blockmodel',
            name='identifiers_condensed',
            field=models.TextField(default='', verbose_name='unique identifier(s) of a block(s) used internally'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blockmodel',
            name='identifiers',
            field=models.TextField(help_text='unique identifier(s) of all variants of a block(s) used internally'),
        ),
        migrations.AlterField(
            model_name='blockmodel',
            name='name',
            field=models.TextField(help_text='name of a block'),
        ),
        migrations.AlterField(
            model_name='blockmodel',
            name='name_cs',
            field=models.TextField(help_text='name of a block', null=True),
        ),
        migrations.AlterField(
            model_name='blockmodel',
            name='name_en',
            field=models.TextField(help_text='name of a block', null=True),
        ),
    ]
