# Generated by Django 4.0.2 on 2022-06-22 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("labour", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="work",
            name="recipe_quantity",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="work",
            name="water_quantity",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
