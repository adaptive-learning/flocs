# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0010_toolbox'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='toolbox',
            options={'ordering': ['level']},
        ),
    ]
