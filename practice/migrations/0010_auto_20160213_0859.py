# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0009_auto_20160212_0441'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskinstancemodel',
            name='session',
            field=models.ForeignKey(to='practice.PracticeSession', null=True, blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='session',
            field=models.OneToOneField(to='practice.PracticeSession', null=True, blank=True, default=None),
        ),
    ]
