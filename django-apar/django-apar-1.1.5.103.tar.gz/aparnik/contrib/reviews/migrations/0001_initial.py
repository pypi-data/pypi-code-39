# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-10-25 15:43


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('basemodels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseReview',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='basemodels.BaseModel')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('is_published', models.BooleanField(default=False, verbose_name='Published')),
            ],
            options={
                'verbose_name': 'Base Review',
                'verbose_name_plural': 'Base Reviews',
            },
            bases=('basemodels.basemodel',),
        ),
    ]
