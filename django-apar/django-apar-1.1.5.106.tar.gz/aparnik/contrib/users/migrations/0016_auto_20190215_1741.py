# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-02-15 17:41


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparnik_users', '0015_auto_20190214_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username_mention',
            field=models.CharField(default='a', max_length=100, unique=True, verbose_name='Username for mention'),
        ),
    ]
