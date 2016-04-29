# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0013_auto_20160429_0302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='level',
        ),
    ]
