# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0005_auto_20160516_0834'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgrammingConcept',
            fields=[
                ('concept_ptr', models.OneToOneField(auto_created=True, parent_link=True, primary_key=True, serialize=False, to='concepts.Concept')),
            ],
            bases=('concepts.concept',),
        ),
        migrations.AddField(
            model_name='concept',
            name='subconcepts',
            field=models.ManyToManyField(to='concepts.Concept', related_name='subconcepts_rel_+'),
        ),
    ]
