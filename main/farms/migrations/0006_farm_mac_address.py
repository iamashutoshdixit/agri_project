# Generated by Django 4.1.3 on 2022-12-06 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("farms", "0005_remove_farmmanagerattendance_datetime_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="farm",
            name="mac_address",
            field=models.CharField(max_length=30, null=True),
        ),
    ]
