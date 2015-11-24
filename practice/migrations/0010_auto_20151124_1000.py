# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0009_auto_20151124_0945'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studenttaskinfomodel',
            old_name='last_solved_instance',
            new_name='last_instance',
        ),
    ]
