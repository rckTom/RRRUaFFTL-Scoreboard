# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0013_auto_20171119_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameresultvalidation',
            name='expiration_date',
            field=models.DateTimeField(null=True),
        ),
    ]