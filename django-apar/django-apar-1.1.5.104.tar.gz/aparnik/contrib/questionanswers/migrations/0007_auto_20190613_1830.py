# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-06-13 18:30


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionanswers', '0006_auto_20190613_1829'),
        ('reviews', '0007_auto_20190613_1829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qa',
            old_name='model_obj2',
            new_name='model_obj',
        ),
    ]
