# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-11-06 16:00


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sliders', '0003_remove_slider_pages'),
    ]

    operations = [
        migrations.CreateModel(
            name='SliderImage',
            fields=[
                ('slider_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sliders.Slider')),
            ],
            options={
                'verbose_name': 'Image Slide Show',
                'manager_inheritance_from_future': True,
                'verbose_name_plural': 'Image Slide Shows',
            },
            bases=('sliders.slider',),
        ),
    ]
