# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-11-03 22:33


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basemodels', '0003_basemodel_update_needed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basemodel',
            name='update_needed',
            field=models.BooleanField(default=False, verbose_name='\\u0646\\u06cc\\u0627\\u0632 \\u0628\\u0647 \\u0628\\u0631\\u0648\\u0632\\u0631\\u0633\\u0627\\u0646\\u06cc'),
        ),
    ]
