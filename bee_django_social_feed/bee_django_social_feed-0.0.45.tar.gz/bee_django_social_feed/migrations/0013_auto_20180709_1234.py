# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-07-09 04:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bee_django_social_feed', '0012_auto_20180709_1210'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'ordering': ['-created_at'], 'permissions': [('can_manage_album', '\u80fd\u8fdb\u5165Albums\u7ba1\u7406\u9875')]},
        ),
    ]
