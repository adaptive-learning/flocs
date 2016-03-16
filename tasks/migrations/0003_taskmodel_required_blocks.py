# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0006_auto_20160307_0406'),
        ('tasks', '0002_auto_20160205_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmodel',
            name='required_blocks',
            field=models.ManyToManyField(to='blocks.BlockModel', help_text='blocks required to solve this task'),
        ),
    ]
