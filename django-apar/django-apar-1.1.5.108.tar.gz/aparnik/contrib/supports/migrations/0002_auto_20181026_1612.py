# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-10-26 16:12


import aparnik.utils.fields
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='support',
            name='phone',
            field=aparnik.utils.fields.PhoneField(blank=True, max_length=255, null=True, validators=[django.core.validators.RegexValidator(code=b'nomatch', message='phone is not valid, please insert with code', regex=b'^0(?!0)\\d{2}([0-9]{8})$')], verbose_name='Phone'),
        ),
    ]
