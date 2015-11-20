# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0004_auto_20151111_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasksdifficultymodel',
            name='solution_count',
            field=models.IntegerField(default=0, verbose_name='How many times the task was solved'),
        ),
        migrations.AlterField(
            model_name='studentsskillmodel',
            name='colors',
            field=models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('-1'), verbose_name='Skill in colors concept'),
        ),
        migrations.AlterField(
            model_name='studentsskillmodel',
            name='conditions',
            field=models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('-1'), verbose_name='Skill in conditions concept'),
        ),
        migrations.AlterField(
            model_name='studentsskillmodel',
            name='logic_expr',
            field=models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('-1'), verbose_name='Skill in logic expressions concept'),
        ),
        migrations.AlterField(
            model_name='studentsskillmodel',
            name='loops',
            field=models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('-1'), verbose_name='Skill in loops concept'),
        ),
        migrations.AlterField(
            model_name='studentsskillmodel',
            name='pits',
            field=models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('-1'), verbose_name='Skill in pits concept'),
        ),
        migrations.AlterField(
            model_name='studentsskillmodel',
            name='programming',
            field=models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('-1'), verbose_name='General skill'),
        ),
        migrations.AlterField(
            model_name='studentsskillmodel',
            name='tokens',
            field=models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('-1'), verbose_name='Skill in tokens concept'),
        ),
        migrations.AlterField(
            model_name='tasksdifficultymodel',
            name='colors',
            field=models.BooleanField(default=False, verbose_name='Difficulty of the colors concept in the task'),
        ),
        migrations.AlterField(
            model_name='tasksdifficultymodel',
            name='conditions',
            field=models.BooleanField(default=False, verbose_name='Difficulty of the conditions concept in the task'),
        ),
        migrations.AlterField(
            model_name='tasksdifficultymodel',
            name='logic_expr',
            field=models.BooleanField(default=False, verbose_name='Difficulty of the logic expressions concept in the task'),
        ),
        migrations.AlterField(
            model_name='tasksdifficultymodel',
            name='loops',
            field=models.BooleanField(default=False, verbose_name='Difficulty of the loops concept in the task'),
        ),
        migrations.AlterField(
            model_name='tasksdifficultymodel',
            name='pits',
            field=models.BooleanField(default=False, verbose_name='Difficulty of the pits concept in the task'),
        ),
        migrations.AlterField(
            model_name='tasksdifficultymodel',
            name='programming',
            field=models.DecimalField(max_digits=4, decimal_places=3, default=0.0, verbose_name='General difficulty of the task'),
        ),
        migrations.AlterField(
            model_name='tasksdifficultymodel',
            name='tokens',
            field=models.BooleanField(default=False, verbose_name='Difficulty of the tokens concept in the task'),
        ),
    ]
