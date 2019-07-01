# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-05-26 12:10


from django.db import migrations
from aparnik.contrib.users.models import DeviceType


def add_keys(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    DeviceLogin = apps.get_model('aparnik_users', 'devicelogin')
    for device in DeviceLogin.objects.all():
        device.device_type = DeviceType.ANDROID if device.device_type_temp == 'a' else DeviceType.IOS
        device.save()


def remove_keys(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    DeviceLogin = apps.get_model('aparnik_users', 'devicelogin')
    for device in DeviceLogin.objects.all():
        device.device_type_temp = 'a' if device.device_type == DeviceType.ANDROID else 'i'
        device.save()


class Migration(migrations.Migration):

    dependencies = [
        ('aparnik_users', '0025_auto_20190526_1210'),
    ]

    operations = [
        migrations.RunPython(add_keys, reverse_code=remove_keys),
    ]
