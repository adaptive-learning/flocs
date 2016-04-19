# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0009_auto_20160419_0651'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concept',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlockConcept',
            fields=[
                ('concept_ptr', models.OneToOneField(to='concepts.Concept', parent_link=True, serialize=False, auto_created=True, primary_key=True)),
                ('block', models.ForeignKey(to='blocks.Block')),
            ],
            bases=('concepts.concept',),
        ),
    ]
