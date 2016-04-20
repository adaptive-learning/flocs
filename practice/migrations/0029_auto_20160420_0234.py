# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0001_initial'),
        ('practice', '0028_auto_20160408_0357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentmodel',
            name='colors',
        ),
        migrations.RemoveField(
            model_name='studentmodel',
            name='conditions',
        ),
        migrations.RemoveField(
            model_name='studentmodel',
            name='logic_expr',
        ),
        migrations.RemoveField(
            model_name='studentmodel',
            name='loops',
        ),
        migrations.RemoveField(
            model_name='studentmodel',
            name='pits',
        ),
        migrations.RemoveField(
            model_name='studentmodel',
            name='programming',
        ),
        migrations.RemoveField(
            model_name='studentmodel',
            name='tokens',
        ),
        migrations.AddField(
            model_name='studentmodel',
            name='_seen_concepts',
            field=models.ManyToManyField(to='concepts.Concept', help_text='concepts already presented to the student'),
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='free_credits',
            field=models.IntegerField(default=0, help_text='number of free credits to spend'),
        ),
        migrations.AlterField(
            model_name='studentmodel',
            name='total_credits',
            field=models.IntegerField(default=0, help_text='total number of credits earned'),
        ),
    ]
