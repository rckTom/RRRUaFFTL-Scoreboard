# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_data',
            field=models.DateTimeField(),
        ),
    ]