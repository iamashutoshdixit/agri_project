# Generated by Django 4.0.2 on 2022-05-30 12:17

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
import pdc.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Batch",
            fields=[
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.CharField(
                        default=pdc.models.generate_id,
                        editable=False,
                        max_length=6,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("crop_name", models.CharField(max_length=20)),
                ("variety", models.CharField(max_length=20)),
                ("sowing_date", models.DateField()),
                ("no_of_seeds", models.IntegerField()),
                ("dome", models.IntegerField(blank=True, null=True)),
                ("transplantation_date", models.DateField(blank=True, null=True)),
                ("no_of_plants", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Batch",
                "verbose_name_plural": "Batches",
            },
        ),
        migrations.CreateModel(
            name="Controller",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("dome", models.IntegerField()),
                (
                    "type",
                    models.IntegerField(
                        choices=[
                            (1, "Exhaust"),
                            (2, "Vent"),
                            (3, "Cooling Pad"),
                            (4, "Shade Net"),
                        ]
                    ),
                ),
                ("device_number", models.IntegerField()),
                ("is_running", models.BooleanField()),
            ],
            options={
                "verbose_name": "Climate Controller",
                "verbose_name_plural": "Climate Controller",
            },
        ),
        migrations.CreateModel(
            name="CoolingPad",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("ph", models.FloatField()),
                ("ec", models.FloatField()),
                ("tank_temperature", models.FloatField()),
                (
                    "remarks",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=50), size=None
                    ),
                ),
            ],
            options={
                "verbose_name": "Cooling Pad",
                "verbose_name_plural": "Cooling Pad",
            },
        ),
        migrations.CreateModel(
            name="DomeParameters",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("dome", models.IntegerField()),
                ("temperature", models.FloatField()),
                ("dry_temperature", models.FloatField()),
                ("wet_temperature", models.FloatField()),
                ("humidity", models.FloatField()),
                ("lux", models.FloatField()),
                ("par_meter", models.FloatField()),
            ],
            options={
                "verbose_name": "Dome Parameters",
                "verbose_name_plural": "Dome Parameters",
            },
        ),
        migrations.CreateModel(
            name="Harvesting",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("dome", models.IntegerField()),
                ("line", models.IntegerField()),
                (
                    "section",
                    models.CharField(
                        choices=[
                            ("A", "Near Cooling Pad"),
                            ("B", "Middle of the Dome"),
                            ("C", "Near Exhaust"),
                        ],
                        max_length=1,
                    ),
                ),
                ("total_weight", models.FloatField()),
                ("pure_weight", models.FloatField()),
                ("wastage_weight", models.FloatField()),
            ],
            options={
                "verbose_name": "Harvesting",
                "verbose_name_plural": "Harvesting",
            },
        ),
        migrations.CreateModel(
            name="HarvestingSample",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("dome", models.IntegerField()),
                ("no_of_fruits", models.IntegerField()),
                ("weight_of_fruits", models.FloatField()),
                ("brix_value", models.FloatField()),
                ("fruit_color", models.CharField(max_length=20)),
            ],
            options={
                "verbose_name": "Harvesting Sample",
                "verbose_name_plural": "Harvesting Samples",
            },
        ),
        migrations.CreateModel(
            name="InnerWaterTank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("dome", models.IntegerField()),
                ("recipe_name", models.CharField(max_length=20)),
                ("ph", models.FloatField()),
                ("ec", models.FloatField()),
                ("do", models.FloatField()),
                ("nutrition_stage", models.CharField(max_length=20)),
                ("temperature", models.FloatField()),
                ("water_quantity", models.FloatField()),
                (
                    "remarks",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=50), size=None
                    ),
                ),
                ("remarks_quantity", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name": "Inner Water Tank",
                "verbose_name_plural": "Inner Water Tank",
            },
        ),
        migrations.CreateModel(
            name="LeafTemperature",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("dome", models.IntegerField()),
                ("line", models.IntegerField()),
                (
                    "section",
                    models.CharField(
                        choices=[
                            ("A", "Near Cooling Pad"),
                            ("B", "Middle of the Dome"),
                            ("C", "Near Exhaust"),
                        ],
                        max_length=1,
                    ),
                ),
                ("temperature", models.FloatField()),
            ],
            options={
                "verbose_name": "Leaf Temperature",
                "verbose_name_plural": "Leaf Temperature",
            },
        ),
        migrations.CreateModel(
            name="NurseryHealth",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("germination", models.DecimalField(decimal_places=2, max_digits=4)),
                ("plant_height", models.FloatField()),
                ("nodes", models.IntegerField()),
                (
                    "remarks",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=50), size=None
                    ),
                ),
                ("observation", models.CharField(max_length=50)),
                (
                    "description",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
            ],
            options={
                "verbose_name": "Nursery Health",
                "verbose_name_plural": "Nursery Health",
            },
        ),
        migrations.CreateModel(
            name="OuterWaterTank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("type", models.IntegerField(choices=[(1, "RO"), (2, "RW")])),
                ("ec", models.FloatField()),
                ("ph", models.FloatField()),
                ("do", models.FloatField()),
                ("temperature", models.FloatField()),
                ("lph", models.FloatField()),
                ("media_filter", models.FloatField()),
                ("pressure", models.FloatField()),
            ],
            options={
                "verbose_name": "Outer Water Tank",
                "verbose_name_plural": "Outer Water Tank",
            },
        ),
        migrations.CreateModel(
            name="OutsideParameters",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("weather", models.CharField(max_length=10)),
                ("wind_speed", models.FloatField()),
                ("wind_direction", models.FloatField()),
                ("temperature", models.FloatField()),
                ("humidity", models.FloatField()),
                ("lux", models.FloatField()),
            ],
            options={
                "verbose_name": "Outside Parameters",
                "verbose_name_plural": "Outside Parameters",
            },
        ),
        migrations.CreateModel(
            name="PlantAnalysis",
            fields=[
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.CharField(
                        default=pdc.models.generate_id,
                        editable=False,
                        max_length=6,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("datetime", models.DateTimeField()),
                ("line", models.IntegerField()),
                ("dome", models.IntegerField()),
                ("section", models.IntegerField()),
                ("image", models.URLField()),
                ("type", models.CharField(max_length=30)),
                ("category", models.CharField(max_length=50)),
                (
                    "remarks",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=50), size=None
                    ),
                ),
                ("comments", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "Plant Analysis",
                "verbose_name_plural": "Plant Analysis",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="PlantFlowering",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("cluster", models.IntegerField()),
                ("flowering", models.JSONField()),
            ],
            options={
                "verbose_name": "Plant Flowering",
                "verbose_name_plural": "Plant Flowering",
            },
        ),
        migrations.CreateModel(
            name="Pollination",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("dome", models.IntegerField()),
                ("line", models.IntegerField()),
                (
                    "section",
                    models.CharField(
                        choices=[
                            ("A", "Near Cooling Pad"),
                            ("B", "Middle of the Dome"),
                            ("C", "Near Exhaust"),
                        ],
                        max_length=1,
                    ),
                ),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                ("count", models.IntegerField()),
            ],
            options={
                "verbose_name": "Pollination",
                "verbose_name_plural": "Pollination",
            },
        ),
        migrations.CreateModel(
            name="RootWeight",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("dome", models.IntegerField()),
                ("line", models.IntegerField()),
                (
                    "section",
                    models.CharField(
                        choices=[
                            ("A", "Near Cooling Pad"),
                            ("B", "Middle of the Dome"),
                            ("C", "Near Exhaust"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "type",
                    models.IntegerField(choices=[(1, "Dry"), (2, "Wet")], default=1),
                ),
                ("weight", models.FloatField()),
            ],
            options={
                "verbose_name": "Root Weight",
                "verbose_name_plural": "Root Weight",
            },
        ),
        migrations.CreateModel(
            name="RootZoneTemperature",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("dome", models.IntegerField()),
                ("line", models.IntegerField()),
                (
                    "section",
                    models.IntegerField(
                        choices=[(1, "Cooling Pad Side"), (2, "Exhaust Side")],
                        default=1,
                    ),
                ),
                ("water_temperature", models.FloatField()),
                ("surface_temperature", models.FloatField()),
            ],
            options={
                "verbose_name": "Root Zone Temperature",
                "verbose_name_plural": "Root Zone Temperature",
            },
        ),
        migrations.CreateModel(
            name="Specimen",
            fields=[
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.CharField(
                        default=pdc.models.generate_id,
                        editable=False,
                        max_length=6,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("position", models.IntegerField()),
                ("chamber", models.IntegerField()),
                ("line", models.IntegerField()),
                ("set", models.IntegerField()),
                ("dome", models.IntegerField()),
            ],
            options={
                "verbose_name": "Specimen",
                "verbose_name_plural": "Specimen",
            },
        ),
        migrations.CreateModel(
            name="SpecimenOutput",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("harvested_fruits", models.IntegerField()),
                ("harvested_weight", models.IntegerField()),
            ],
            options={
                "verbose_name": "Specimen Output",
                "verbose_name_plural": "Specimen Output",
            },
        ),
        migrations.CreateModel(
            name="VegetativeGrowth",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("datetime", models.DateTimeField(default=datetime.datetime.now)),
                ("plant_height", models.FloatField()),
                ("stem_diameter", models.FloatField()),
                ("no_of_branches", models.IntegerField()),
                ("no_of_branch_nodes", models.IntegerField()),
                ("internode_distance", models.FloatField(blank=True, null=True)),
                ("nodes", models.IntegerField(blank=True, null=True)),
                ("fruit_distance", models.FloatField()),
                ("no_of_petioles", models.IntegerField()),
                ("length_of_petioles", models.FloatField()),
                ("leaves_in_petioles", models.IntegerField()),
            ],
            options={
                "verbose_name": "Vegetative Growth",
                "verbose_name_plural": "Vegetative Growth",
            },
        ),
    ]
