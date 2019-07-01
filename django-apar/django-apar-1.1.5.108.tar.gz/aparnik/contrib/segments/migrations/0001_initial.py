# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-10-25 15:43


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('basemodels', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseSegment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='Title')),
                ('is_active', models.BooleanField(default=True, verbose_name='\\u0641\\u0639\\u0627\\u0644')),
                ('sort', models.IntegerField(default=0, verbose_name='Sort')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Update at')),
                ('model_obj', models.ManyToManyField(to='basemodels.BaseModel', verbose_name='Model')),
                ('pages', models.ManyToManyField(blank=True, related_name='segment_pages', to='pages.Page', verbose_name='Page')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_segments.basesegment_set+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Base Segment',
                'verbose_name_plural': 'Bases Segments',
            },
        ),
    ]
