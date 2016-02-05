# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmodel',
            name='title',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taskmodel',
            name='title_cs',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='taskmodel',
            name='title_en',
            field=models.TextField(null=True),
        ),
    ]
