# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-04-28 16:44


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_auto_20190428_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basecourse',
            name='description',
        ),
    ]
