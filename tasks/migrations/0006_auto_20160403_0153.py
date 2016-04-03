# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20160402_0446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmodel',
            name='level',
            field=models.ForeignKey(help_text='minimum level required to attempt this task', to='levels.Level', null=True, default=None),
        ),
    ]
