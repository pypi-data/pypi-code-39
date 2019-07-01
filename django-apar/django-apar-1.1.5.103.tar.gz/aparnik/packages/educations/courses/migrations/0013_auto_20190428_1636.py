# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-04-28 16:36


from django.db import migrations


def add_keys(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    BaseCourse = apps.get_model('courses', 'BaseCourse')
    try:
        for course in BaseCourse.objects.all():
            course.content = course.description
            course.save()
    except Exception:
        pass


def remove_keys(apps, schema_editor):
    '''
    We can't import the Post model directly as it may be a newer
    version than this migration expects. We use the historical version.
    '''
    BaseCourse = apps.get_model('courses', 'BaseCourse')
    try:
        for course in BaseCourse.objects.all():
            course.description = course.content
            course.save()
    except Exception:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_basecourse_content'),
    ]

    operations = [
        migrations.RunPython(add_keys, reverse_code=remove_keys),
    ]
