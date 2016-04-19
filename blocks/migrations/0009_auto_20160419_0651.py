# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0008_auto_20160402_0404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.TextField(help_text='name of a block shown to students')),
                ('name_cs', models.TextField(help_text='name of a block shown to students', null=True)),
                ('name_en', models.TextField(help_text='name of a block shown to students', null=True)),
                ('identifier', models.CharField(help_text='short unique identifier of the block', max_length=50, unique=True)),
                ('_expanded_identifiers', models.TextField(help_text='JSON array of identifiers for all variants of the block(null if there are no extra variants)', null=True, default=None)),
                ('level', models.SmallIntegerField(help_text='level required to use this block', default=1)),
            ],
        ),
        migrations.DeleteModel(
            name='BlockModel',
        ),
    ]
