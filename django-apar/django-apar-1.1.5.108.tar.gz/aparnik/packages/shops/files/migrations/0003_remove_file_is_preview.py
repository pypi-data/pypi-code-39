# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-10-28 17:32


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_auto_20181026_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='is_preview',
        ),
    ]
