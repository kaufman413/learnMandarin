# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-26 21:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_prompt_promptid'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='vars',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
