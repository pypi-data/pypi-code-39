# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-05-01 17:10


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_remove_basecourse_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursefile',
            name='time',
        ),
    ]
