# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-11-14 15:24


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20181114_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='further_details',
            field=models.TextField(blank=True, null=True, verbose_name='Extra Description'),
        ),
    ]
