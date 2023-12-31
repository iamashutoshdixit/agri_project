# Generated by Django 4.1.3 on 2022-12-29 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pdc", "0013_batch_latitude_batch_longitude_controller_latitude_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="innerwatertank",
            name="additional_details",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="innerwatertank",
            name="ph_correction",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="innerwatertank",
            name="quantity",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="innerwatertank",
            name="unit",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="leafareadetection",
            name="leaf_breadth",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="leafareadetection",
            name="leaf_length",
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name="leafareadetection",
            name="template_length_breadth",
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name="reproductivegrowth",
            name="stem",
            field=models.IntegerField(
                blank=True, choices=[(1, "A"), (2, "B")], null=True
            ),
        ),
        migrations.AlterField(
            model_name="innerwatertank",
            name="remarks_quantity",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
