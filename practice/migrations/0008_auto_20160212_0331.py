# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0007_auto_20160206_1218'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StudentsSkillModel',
            new_name='StudentModel',
        ),
    ]
