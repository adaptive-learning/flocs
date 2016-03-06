# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0002_auto_20160305_1259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blockmodel',
            name='identifier',
        ),
        migrations.AddField(
            model_name='blockmodel',
            name='identifiers',
            field=models.TextField(verbose_name='unique identifier(s) of a block(s) used internally', default='{"identifiers":[]}'),
        ),
    ]
