# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0002_environmentconcept_gameconcept'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('text', models.TextField(help_text='Text of the instruction shown in the game.')),
                ('text_cs', models.TextField(help_text='Text of the instruction shown in the game.', null=True)),
                ('text_en', models.TextField(help_text='Text of the instruction shown in the game.', null=True)),
                ('concept', models.ForeignKey(to='concepts.Concept')),
            ],
        ),
    ]
