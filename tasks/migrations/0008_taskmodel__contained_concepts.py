# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0002_environmentconcept_gameconcept'),
        ('tasks', '0007_auto_20160403_0324'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmodel',
            name='_contained_concepts',
            field=models.ManyToManyField(help_text='concepts contained in the task', to='concepts.Concept'),
        ),
    ]
