# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0021_auto_20160305_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentmodel',
            name='available_blocks',
            field=models.ManyToManyField(verbose_name='blocks that has been purchased by the student', to='blocks.Block'),
        ),
    ]
