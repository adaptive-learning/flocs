# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0030_auto_20160426_0825'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InstructionsModel',
        ),
    ]
