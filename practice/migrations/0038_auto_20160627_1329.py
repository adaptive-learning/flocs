# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0037_practicesession_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskinstancemodel',
            name='blocks',
            field=models.ManyToManyField(to='blocks.Block', help_text='all blocks in toolbox (but only those required by the task were available)'),
        ),
    ]
