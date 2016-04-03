# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0025_auto_20160330_0400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentmodel',
            name='available_blocks',
        ),
    ]
