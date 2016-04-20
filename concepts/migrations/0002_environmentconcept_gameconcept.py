# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnvironmentConcept',
            fields=[
                ('concept_ptr', models.OneToOneField(auto_created=True, to='concepts.Concept', parent_link=True, serialize=False, primary_key=True)),
            ],
            bases=('concepts.concept',),
        ),
        migrations.CreateModel(
            name='GameConcept',
            fields=[
                ('concept_ptr', models.OneToOneField(auto_created=True, to='concepts.Concept', parent_link=True, serialize=False, primary_key=True)),
                ('checker', models.TextField(default=None, help_text='name of a Task method which check if it contains this concept', null=True)),
            ],
            bases=('concepts.concept',),
        ),
    ]
