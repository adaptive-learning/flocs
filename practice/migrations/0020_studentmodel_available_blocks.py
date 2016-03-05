# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0001_initial'),
        ('practice', '0019_auto_20160302_0422'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='available_blocks',
            field=models.ManyToManyField(verbose_name='blocks that has been purchased by the student', to='blocks.BlockModel'),
        ),
    ]
