# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-03-24 13:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bee_django_social_feed', '0017_feedcomment_to_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='type_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
