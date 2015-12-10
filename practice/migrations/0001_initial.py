# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructionsModel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('flow_factor', models.SmallIntegerField(choices=[(255, 'instructions on basics of the game'), (4, 'instructions concerning logical expresions'), (5, 'instructions concerning colors'), (6, 'instructions concerning tokens'), (7, 'instructions concerning pits'), (2, 'instructions concerning loops'), (3, 'instructions on how to use conditions')], unique=True, default=255, verbose_name='Factor to which these instructions belong')),
                ('text', models.CharField(max_length=255, verbose_name='Text of instruction shown in game page')),
            ],
        ),
        migrations.CreateModel(
            name='StudentsSkillModel',
            fields=[
                ('student', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('programming', models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('-1'), verbose_name='General skill')),
                ('conditions', models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('-1'), verbose_name='Skill in conditions concept')),
                ('loops', models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('-1'), verbose_name='Skill in loops concept')),
                ('logic_expr', models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('-1'), verbose_name='Skill in logic expressions concept')),
                ('colors', models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('-1'), verbose_name='Skill in colors concept')),
                ('tokens', models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('-1'), verbose_name='Skill in tokens concept')),
                ('pits', models.DecimalField(max_digits=4, decimal_places=3, default=Decimal('-1'), verbose_name='Skill in pits concept')),
            ],
        ),
        migrations.CreateModel(
            name='StudentTaskInfoModel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TaskInstanceModel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('time_start', models.DateTimeField(default=datetime.datetime.now)),
                ('time_end', models.DateTimeField(null=True, default=None)),
                ('time_spent', models.IntegerField(default=0)),
                ('solved', models.BooleanField(default=False)),
                ('reported_flow', models.SmallIntegerField(choices=[(0, 'unknown'), (1, 'too difficult'), (2, 'just right'), (3, 'too easy')], default=0)),
                ('predicted_flow', models.FloatField()),
                ('attempt_count', models.IntegerField(default=0)),
                ('student', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TasksDifficultyModel',
            fields=[
                ('task', models.OneToOneField(primary_key=True, serialize=False, to='tasks.TaskModel')),
                ('programming', models.DecimalField(max_digits=4, decimal_places=3, default=0.0, verbose_name='General difficulty of the task')),
                ('conditions', models.BooleanField(default=False, verbose_name='Difficulty of the conditions concept in the task')),
                ('loops', models.BooleanField(default=False, verbose_name='Difficulty of the loops concept in the task')),
                ('logic_expr', models.BooleanField(default=False, verbose_name='Difficulty of the logic expressions concept in the task')),
                ('colors', models.BooleanField(default=False, verbose_name='Difficulty of the colors concept in the task')),
                ('tokens', models.BooleanField(default=False, verbose_name='Difficulty of the tokens concept in the task')),
                ('pits', models.BooleanField(default=False, verbose_name='Difficulty of the pits concept in the task')),
                ('solution_count', models.IntegerField(default=0, verbose_name='How many times the task was solved')),
            ],
        ),
        migrations.AddField(
            model_name='taskinstancemodel',
            name='task',
            field=models.ForeignKey(to='tasks.TaskModel'),
        ),
        migrations.AddField(
            model_name='studenttaskinfomodel',
            name='last_instance',
            field=models.ForeignKey(default=None, null=True, to='practice.TaskInstanceModel'),
        ),
        migrations.AddField(
            model_name='studenttaskinfomodel',
            name='student',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='studenttaskinfomodel',
            name='task',
            field=models.ForeignKey(to='tasks.TaskModel'),
        ),
        migrations.AlterUniqueTogether(
            name='studenttaskinfomodel',
            unique_together=set([('student', 'task')]),
        ),
        migrations.AlterIndexTogether(
            name='studenttaskinfomodel',
            index_together=set([('student', 'task')]),
        ),
    ]
