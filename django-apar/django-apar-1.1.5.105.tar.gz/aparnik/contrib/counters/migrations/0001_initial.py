# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-01-14 17:14


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('basemodels', '0010_basemodel_visit_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('v', 'Visiting'), ('s', 'Sharing')], max_length=2, verbose_name='Action kind')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update at')),
                ('model_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basemodels.BaseModel', verbose_name='Base Model')),
                ('user_obj', models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Counter',
                'verbose_name_plural': 'Counters',
            },
        ),
    ]
