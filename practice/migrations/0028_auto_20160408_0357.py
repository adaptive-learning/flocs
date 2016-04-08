# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0027_studentmodel_level'),
    ]

    operations = [
        migrations.RenameField(
            model_name='practicesession',
            old_name='active',
            new_name='_active',
        ),
    ]
