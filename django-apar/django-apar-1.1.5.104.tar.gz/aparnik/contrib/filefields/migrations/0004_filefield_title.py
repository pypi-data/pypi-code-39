# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-10-26 18:26


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filefields', '0003_auto_20181026_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='filefield',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='\\u0639\\u0646\\u0648\\u0627\\u0646'),
        ),
    ]
