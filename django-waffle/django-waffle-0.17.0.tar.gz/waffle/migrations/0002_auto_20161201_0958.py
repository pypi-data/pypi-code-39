# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 09:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waffle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='switch',
            name='active',
            field=models.BooleanField(default=False, help_text='Is this switch active?'),
        ),
    ]
