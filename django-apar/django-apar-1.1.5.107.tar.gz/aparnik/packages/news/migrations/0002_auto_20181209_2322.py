# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-12-09 23:22


from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='publish_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\\u062a\\u0627\\u0631\\u06cc\\u062e \\u0627\\u0646\\u062a\\u0634\\u0627\\u0631'),
        ),
    ]
