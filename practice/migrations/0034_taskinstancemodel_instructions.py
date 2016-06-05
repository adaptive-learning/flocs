# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0006_auto_20160517_1241'),
        ('practice', '0033_auto_20160520_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskinstancemodel',
            name='instructions',
            field=models.ManyToManyField(help_text='instructions presented to the student', to='concepts.Instruction'),
        ),
    ]
