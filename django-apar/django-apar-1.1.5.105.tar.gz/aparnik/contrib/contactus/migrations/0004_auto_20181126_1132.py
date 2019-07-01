# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-11-26 11:32


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basemodels', '0004_auto_20181103_2233'),
        ('contactus', '0003_auto_20181126_1132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactus',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='contactus',
            name='id',
        ),
        migrations.RemoveField(
            model_name='contactus',
            name='update_at',
        ),
        migrations.AddField(
            model_name='contactus',
            name='basemodel_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='basemodels.BaseModel'),
            preserve_default=False,
        ),
    ]
