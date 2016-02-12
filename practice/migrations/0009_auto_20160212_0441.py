# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0008_auto_20160212_0331'),
    ]

    operations = [
        migrations.CreateModel(
            name='PracticeSession',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
            ],
        ),
        migrations.RenameField(
            model_name='studentmodel',
            old_name='student',
            new_name='user',
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='session',
            field=models.OneToOneField(blank=True, to='practice.PracticeSession', null=True),
        ),
    ]
