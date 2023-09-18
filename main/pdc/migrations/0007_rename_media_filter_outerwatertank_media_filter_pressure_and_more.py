# Generated by Django 4.0.4 on 2022-10-11 14:12

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdc', '0006_remove_harvesting_stage_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='outerwatertank',
            old_name='media_filter',
            new_name='media_filter_pressure',
        ),
        migrations.AddField(
            model_name='controller',
            name='ventilationType',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='outerwatertank',
            name='primary_membrane_filter_pressure',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='controller',
            name='device_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='controller',
            name='type',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='harvesting',
            name='photo',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='harvesting',
            name='section',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='innerwatertank',
            name='do',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='innerwatertank',
            name='nutrition_stage',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='leaftemperature',
            name='section',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='nurseryhealth',
            name='photo',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='outerwatertank',
            name='do',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='outerwatertank',
            name='pressure',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='outsideparameters',
            name='wind_direction',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='pollination',
            name='section',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='rootweight',
            name='section',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='rootzonetemperature',
            name='section',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='vegetativegrowth',
            name='photo',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, null=True, size=None),
        ),
    ]