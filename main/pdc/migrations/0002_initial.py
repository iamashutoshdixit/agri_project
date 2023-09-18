# Generated by Django 4.0.2 on 2022-05-30 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("pdc", "0001_initial"),
        ("farms", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="vegetativegrowth",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="vegetativegrowth",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="vegetativegrowth",
            name="specimen",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="pdc.specimen"
            ),
        ),
        migrations.AddField(
            model_name="specimenoutput",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="specimenoutput",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="specimenoutput",
            name="specimen",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="pdc.specimen"
            ),
        ),
        migrations.AddField(
            model_name="specimen",
            name="batch",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, to="pdc.batch"
            ),
        ),
        migrations.AddField(
            model_name="specimen",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="rootzonetemperature",
            name="batch",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, to="pdc.batch"
            ),
        ),
        migrations.AddField(
            model_name="rootzonetemperature",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="rootzonetemperature",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="rootweight",
            name="batch",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, to="pdc.batch"
            ),
        ),
        migrations.AddField(
            model_name="rootweight",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="rootweight",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="pollination",
            name="batch",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, to="pdc.batch"
            ),
        ),
        migrations.AddField(
            model_name="pollination",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="pollination",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="plantflowering",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="plantflowering",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="plantflowering",
            name="specimen",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="pdc.specimen"
            ),
        ),
        migrations.AddField(
            model_name="plantanalysis",
            name="batch",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="pdc.batch"
            ),
        ),
        migrations.AddField(
            model_name="plantanalysis",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="outsideparameters",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="outsideparameters",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="outerwatertank",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="outerwatertank",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="nurseryhealth",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="nurseryhealth",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="nurseryhealth",
            name="specimen",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="pdc.specimen"
            ),
        ),
        migrations.AddField(
            model_name="leaftemperature",
            name="batch",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, to="pdc.batch"
            ),
        ),
        migrations.AddField(
            model_name="leaftemperature",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="leaftemperature",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="innerwatertank",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="innerwatertank",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="harvestingsample",
            name="batch",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="pdc.batch"
            ),
        ),
        migrations.AddField(
            model_name="harvestingsample",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="harvestingsample",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="harvesting",
            name="batch",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.PROTECT, to="pdc.batch"
            ),
        ),
        migrations.AddField(
            model_name="harvesting",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="harvesting",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="domeparameters",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="domeparameters",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="coolingpad",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="coolingpad",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="controller",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="controller",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
        migrations.AddField(
            model_name="batch",
            name="commercial_farm",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="commercial_farm",
                to="farms.farm",
            ),
        ),
        migrations.AddField(
            model_name="batch",
            name="farm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="farms.farm"
            ),
        ),
    ]