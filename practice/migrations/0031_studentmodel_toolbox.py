# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import practice.models.student


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0013_auto_20160429_0302'),
        ('practice', '0030_auto_20160426_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmodel',
            name='toolbox',
            field=models.ForeignKey(null=True, to='blocks.Toolbox', default=practice.models.student._get_initial_toolbox, help_text='blocks available to the student'),
        ),
    ]
