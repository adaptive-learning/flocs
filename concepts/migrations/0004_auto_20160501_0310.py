# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('concepts', '0003_instruction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instruction',
            name='text',
            field=models.TextField(help_text='Text of the instruction shown to the student.'),
        ),
        migrations.AlterField(
            model_name='instruction',
            name='text_cs',
            field=models.TextField(null=True, help_text='Text of the instruction shown to the student.'),
        ),
        migrations.AlterField(
            model_name='instruction',
            name='text_en',
            field=models.TextField(null=True, help_text='Text of the instruction shown to the student.'),
        ),
    ]
