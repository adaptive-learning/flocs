# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('practice', '0002_tasksdifficultymodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentsSkillModel',
            fields=[
                ('student', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('programming', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='General skill')),
                ('conditions', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Skill in conditions concept')),
                ('loops', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Skill in loops concept')),
                ('logic_expr', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Skill in logic expressions concept')),
                ('colors', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Skill in colors concept')),
                ('tokens', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Skill in tokens concept')),
                ('pits', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Skill in pits concept')),
            ],
        ),
        migrations.AlterField(
            model_name='tasksdifficultymodel',
            name='colors',
            field=models.BooleanField(verbose_name='Difficulty of the colors concept in the task'),
        ),
        migrations.AlterField(
            model_name='tasksdifficultymodel',
            name='conditions',
            field=models.BooleanField(verbose_name='Difficulty of the conditions concept in the task'),
        ),
        migrations.AlterField(
            model_name='tasksdifficultymodel',
            name='logic_expr',
            field=models.BooleanField(verbose_name='Difficulty of the logic expressions concept in the task'),
        ),
        migrations.AlterField(
            model_name='tasksdifficultymodel',
            name='loops',
            field=models.BooleanField(verbose_name='Difficulty of the loops concept in the task'),
        ),
        migrations.AlterField(
            model_name='tasksdifficultymodel',
            name='pits',
            field=models.BooleanField(verbose_name='Difficulty of the pits concept in the task'),
        ),
        migrations.AlterField(
            model_name='tasksdifficultymodel',
            name='tokens',
            field=models.BooleanField(verbose_name='Difficulty of the tokens concept in the task'),
        ),
    ]
