# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-11-30 16:41


import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparnik_users', '0008_auto_20181026_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='co_sale_percentage_value',
            field=models.PositiveIntegerField(default=0, help_text='If the number is set to 0, then the value in the settings will apply', validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)], verbose_name='Co Sale Percentage'),
        ),
    ]
