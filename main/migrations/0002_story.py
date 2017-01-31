# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-26 17:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('firstPrompt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='firstPrompt', to='main.Prompt')),
            ],
        ),
    ]
