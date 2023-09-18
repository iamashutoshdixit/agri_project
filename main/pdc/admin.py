# python imports
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.urls import path

# user imports
from libs.mixins import (
    PermissionMixin,
    ExportCsvMixin,
    ImportCsvMixin,
)
from .forms import ChangeBatchStatus, ChangeSpecimenStatus
from .models import (
    NurseryHealth,
    VegetativeGrowth,
    ReproductiveGrowth,
    SpecimenOutput,
    Pollination,
    Harvesting,
    HarvestingSample,
    RootWeight,
    LeafTemperature,
    RootZoneTemperature,
    OutsideParameters,
    DomeParameters,
    Controller,
    OuterWaterTank,
    InnerWaterTank,
    CoolingPad,
    Batch,
    Specimen,
    PlantAnalysis,
    LeafAreaDetection,
)

# GROUPS for grouping in custom admin page
GROUPS = {
    "pdc": [
        "Specimen",
        "Batch",
    ],
    "specimen": [
        "NurseryHealth",
        "VegetativeGrowth",
        "ReproductiveGrowth",
        "SpecimenOutput",
        "LeafAreaDetection",
    ],
    "dome": [
        "PlantAnalysis",
        "Pollination",
        "Harvesting",
        "HarvestingSample",
        "RootWeight",
        "LeafTemperature",
        "RootZoneTemperature",
    ],
    "climate": [
        "OutsideParameters",
        "DomeParameters",
        "Controller",
    ],
    "irrigation": [
        "OuterWaterTank",
        "InnerWaterTank",
        "CoolingPad",
    ],
}

# Register your models here.


class CustomAdminSite(admin.AdminSite):
    site_header = "Eekifoods Administration"
    index_title = "ERP Management"
    site_title = "Eekifoods Administration"

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

        pdc = list(filter(lambda app: app["app_label"] == "pdc", app_list))
        if len(pdc) > 0:
            pdc = pdc[0]
            app_models = pdc["models"]

            app_groups = []

            for group, models in GROUPS.items():
                temp = list(
                    filter(
                        lambda m: m["object_name"] in models,
                        app_models,
                    )
                )
                temp.sort(key=lambda x: x["name"])
                app_groups.append(
                    {
                        "group_label": group,
                        "models": temp,
                    }
                )

            pdc["groups"] = app_groups
            pdc["models"] = []

        # Sort the models alphabetically within each app.
        for app in app_list:
            app["models"].sort(key=lambda x: x["name"])

        # return app list with grouped models
        return app_list


class SpecimenAdmin(
    PermissionMixin,
    ExportCsvMixin,
    ImportCsvMixin,
):
    list_display = (
        "id",
        "farm",
        "batch",
        "position",
        "line",
        "set",
        "dome",
        "created_at",
    )
    search_fields = ["id", "batch"]
    list_filter = [
        "farm",
    ]
    ordering = ["-created_at"]
    actions = ["change_status", "export_selected"]

    csv_fields = [
        "id",
        "created_by.id",
        "created_at",
        "batch.id",
        "line",
        "position",
        "is_active",
        "longitude",
        "latitude",
        "farm.id",
        "chamber",
        "set",
        "dome",
        "remarks",
        "decommission_date",
        "decommission_by.id",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def change_status(self, request, queryset):
        if "set_specimen_status" in request.POST:
            form = ChangeSpecimenStatus(request.POST)
            if form.is_valid():
                for obj in queryset:
                    is_active = form.cleaned_data["is_active"]
                    remarks = form.cleaned_data["remarks"]
                    decom_date = form.cleaned_data["decommission_date"]
                    decom_by = request.user
                    if is_active:
                        decom_date = None
                        decom_by = None
                    if not is_active:
                        message = f"Decommissioned on {decom_date} - {remarks}"
                    else:
                        message = f"Re-commissioned - {remarks}"
                    ctype = ContentType.objects.get_for_model(Specimen)
                    LogEntry.objects.log_action(
                        user_id=request.user.id,
                        content_type_id=ctype.id,
                        object_id=obj.id,
                        object_repr=str(obj),
                        change_message=message,
                        action_flag=CHANGE,
                    )
                    obj.is_active = is_active
                    obj.decommission_date = decom_date
                    obj.decommission_by = decom_by
                    obj.remarks = remarks
                    obj.save()
                return HttpResponseRedirect(".")
        else:
            form = ChangeSpecimenStatus(
                initial={
                    "is_active": queryset[0].is_active,
                }
            )
        context = {
            "title": "Change status of specimen",
            "objects": queryset,
            "form": form,
        }
        return render(request, "pdc/specimen/change-status.html", context)

    class Meta:
        model = Specimen


class BatchAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = (
        "farm",
        "id",
        "commercial_farm",
        "crop_name",
        "variety",
        "sowing_date",
        "no_of_seeds",
        "dome",
        "transplantation_date",
        "no_of_plants",
        "is_active",
        "created_at",
    )
    search_fields = ["id"]
    ordering = ["-created_at"]
    list_filter = [
        "farm",
        "commercial_farm",
        "is_active",
    ]
    actions = ["change_status", "export_selected"]
    csv_fields = [
        "id",
        "created_by.id",
        "created_at",
        "batch.id",
        "no_of_seeds",
        "sowing_date",
        "is_active",
        "longitude",
        "latitude",
        "farm.id",
        "commercial_farm.id",
        "variety",
        "crop_name",
        "dome",
        "remarks",
        "decommission_date",
        "decommission_by.id",
        "transplantation_date",
        "no_of_plants",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def change_status(self, request, queryset):
        if "set_batch_status" in request.POST:
            form = ChangeBatchStatus(request.POST)
            if form.is_valid():
                obj = queryset[0]
                for obj in queryset:
                    is_active = form.cleaned_data["is_active"]
                    remarks = form.cleaned_data["remarks"]
                    decom_date = form.cleaned_data["decommission_date"]
                    decom_by = request.user
                    if is_active:
                        decom_date = None
                        decom_by = None
                    if not is_active:
                        message = f"Decommissioned on {decom_date} - {remarks}"
                    else:
                        message = f"Re-commissioned - {remarks}"
                    ctype = ContentType.objects.get_for_model(Batch)
                    LogEntry.objects.log_action(
                        user_id=request.user.id,
                        content_type_id=ctype.id,
                        object_id=obj.id,
                        object_repr=str(obj),
                        change_message=message,
                        action_flag=CHANGE,
                    )
                    obj.is_active = is_active
                    obj.decommission_date = decom_date
                    obj.decommission_by = decom_by
                    obj.remarks = remarks
                    obj.save()
                return HttpResponseRedirect(".")
        else:
            form = ChangeBatchStatus(
                initial={
                    "is_active": queryset[0].is_active,
                }
            )
        context = {
            "title": "Change status of batch",
            "objects": queryset,
            "form": form,
        }
        return render(request, "pdc/batch/change-status.html", context)

    class Meta:
        model = Batch


class PlantAnalysisAdmin(PermissionMixin):
    list_display = (
        "farm",
        "batch",
        "dome",
        "line",
        "section",
        # "image",
        "category",
        # "remarks",
        "created_at",
    )
    ordering = ["-created_at"]
    list_filter = [
        "farm",
    ]
    readonly_fields = ["photo_urls"]


class NurseryHealthAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "specimen",
        "germination",
        "plant_height",
        "nodes",
        # "remarks",
        "observation",
        "created_at",
    ]
    list_filter = [
        "farm",
    ]
    ordering = ["-created_at"]
    readonly_fields = ["photo_urls"]
    actions = ["export_selected"]

    csv_fields = [
        "id",
        "created_by.id",
        "specimen.id",
        "created_at",
        "is_active",
        "longitude",
        "latitude",
        "farm.id",
        "germination",
        "remarks",
        "nodes",
        "remarks",
        "observation",
        "plant_height",
        "photo",
        "description",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = NurseryHealth


class VegetativeGrowthAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "specimen",
        "plant_height",
        "stem_diameter",
        "internode_distance",
        "nodes",
        "no_of_branches",
        "no_of_branch_nodes",
        "created_at",
    ]
    list_filter = [
        "farm",
    ]
    ordering = ["-created_at"]
    readonly_fields = ["photo_urls"]
    actions = ["export_selected"]

    csv_fields = [
        "id",
        "created_by.id",
        "created_at",
        "specimen.id",
        "is_active",
        "longitude",
        "latitude",
        "farm.id",
        "plant_height",
        "stem_diameter",
        "stem_diameter_2",
        "no_of_branches",
        "no_of_branch_nodes",
        "internode_distance",
        "fruit_distance",
        "no_of_petioles",
        "length_of_petioles",
        "leaves_in_petioles",
        "description",
        "remarks",
        "photo",
        "stem",
        "nodes",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = ReproductiveGrowth


class ReproductiveGrowthAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "specimen",
        "cluster",
        # "female_flowers",
        # "fruits",
        "created_at",
    ]
    list_filter = [
        "farm",
    ]
    actions = ["export_selected"]
    ordering = ["-created_at"]

    csv_fields = [
        "id",
        "created_by.id",
        "created_at",
        "specimen.id",
        "is_active",
        "longitude",
        "latitude",
        "farm.id",
        "remarks",
        "cluster",
        "flowering",
        "stem",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = ReproductiveGrowth


class SpecimenOutputAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "specimen",
        "harvested_fruits",
        "harvested_weight",
        "created_at",
    ]
    list_filter = [
        "farm",
    ]
    actions = ["export_selected"]
    ordering = ["-created_at"]

    csv_fields = [
        "id",
        "created_by.id",
        "created_at",
        "specimen.id",
        "is_active",
        "longitude",
        "latitude",
        "farm.id",
        "stage_of_harvest",
        "harvested_fruits",
        "harvested_weight",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = SpecimenOutput


class PollinationAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "dome",
        "line",
        "section",
        "start_time",
        "end_time",
        "count",
        "created_at",
    ]
    list_filter = [
        "farm",
        "section",
        "dome",
    ]
    ordering = ["-created_at"]
    actions = ["export_selected"]

    csv_fields = [
        "id",
        "created_by.id",
        "created_at",
        "batch.id",
        "is_active",
        "longitude",
        "latitude",
        "farm.id",
        "start_time",
        "end_time",
        "section",
        "count",
        "dome",
        "line",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = Pollination


class HarvestingAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "dome",
        "line",
        "variety",
        "total_weight",
        "pure_weight",
        "wastage_weight",
        "created_at",
    ]
    list_filter = [
        "farm",
        "variety",
        "dome",
    ]
    ordering = ["-created_at"]
    readonly_fields = ["photo_urls"]
    actions = ["export_selected"]

    csv_fields = [
        "id",
        "created_by.id",
        "created_at",
        "batch.id",
        "farm.id",
        "is_active",
        "longitude",
        "latitude",
        "line",
        "variety",
        "total_weight",
        "photo",
        "brix_value",
        "pure_weight",
        "wastage_weight",
        "remarks",
        "average_weight",
        "dome",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = Harvesting


class HarvestingSampleAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "batch",
        "dome",
        "no_of_fruits",
        "weight_of_fruits",
        "fruit_color",
        "created_at",
    ]
    list_filter = [
        "farm",
        "dome",
    ]
    ordering = ["-created_at"]
    actions = ["export_selected"]

    csv_fields = [
        "id",
        "created_by.id",
        "created_at",
        "batch.id",
        "is_active",
        "longitude",
        "latitude",
        "farm.id",
        "no_of_fruits",
        "weight_of_fruits",
        "brix_value",
        "fruit_color",
        "dome",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = HarvestingSample


class RootWeightAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "dome",
        "line",
        "section",
        "type",
        "weight",
        "created_at",
    ]
    list_filter = [
        "farm",
        "section",
        "dome",
    ]
    ordering = ["-created_at"]
    actions = ["export_selected"]

    csv_fields = [
        "id",
        "created_by.id",
        "created_at",
        "batch.id",
        "is_active",
        "longitude",
        "latitude",
        "farm.id",
        "line",
        "dome",
        "section",
        "type",
        "weight",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = RootWeight


class LeafTemperatureAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "dome",
        "line",
        "section",
        "temperature",
        "created_at",
    ]
    list_filter = [
        "farm",
    ]
    ordering = ["-created_at"]
    actions = ["export_selected"]

    csv_fields = [
        "id",
        "created_by.id",
        "created_at",
        "line",
        "temperature",
        "section",
        "is_active",
        "longitude",
        "latitude",
        "farm.id",
        "dome",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = LeafTemperature


class RootZoneTemperatureAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "dome",
        "line",
        "section",
        "water_temperature_in_c",
        "surface_temperature_in_c",
        "created_at",
    ]
    list_filter = [
        "farm",
        "section",
        "dome",
    ]
    ordering = ["-created_at"]
    actions = ["export_selected"]

    csv_fields = [
        "id",
        "is_active",
        "created_by.id",
        "created_at",
        "longitude",
        "latitude",
        "farm.id",
        "batch.id",
        "line",
        "section",
        "water_temperature",
        "surface_temperature",
        "dome",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = RootZoneTemperature


class OutsideParametersAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "weather",
        "wind_speed_in_km_hr",
        "wind_direction",
        "temperature_in_c",
        "humidity_in_p",
        "lux_in_lux",
        "created_at",
    ]
    list_filter = [
        "farm",
    ]
    ordering = ["-created_at"]
    actions = ["export_selected"]

    csv_fields = [
        "id",
        "is_active",
        "created_by.id",
        "created_at",
        "longitude",
        "latitude",
        "farm.id",
        "weather",
        "temperature",
        "humidity",
        "lux",
        "wind_speed",
        "wind_direction",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = OutsideParameters


class DomeParametersAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "dome",
        "temperature_in_c",
        "dry_temperature_in_c",
        "wet_temperature_in_c",
        "humidity_in_p",
        "lux_in_lux",
        "par_meter",
        "created_at",
    ]
    list_filter = [
        "farm",
        "dome",
    ]
    ordering = ["-created_at"]
    actions = ["export_selected"]

    csv_fields = [
        "id",
        "is_active",
        "created_by.id",
        "created_at",
        "longitude",
        "latitude",
        "farm.id",
        "temperature",
        "dry_temperature",
        "wet_temperature",
        "humidity",
        "par_meter",
        "dome",
        "lux",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = DomeParameters


class ControllerAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "dome",
        "type",
        "device_number",
        "is_running",
        "created_at",
    ]
    list_filter = [
        "farm",
        "type",
        "dome",
    ]
    ordering = ["-created_at"]
    actions = ["export_selected"]

    csv_fields = [
        "id",
        "is_active",
        "created_by.id",
        "created_at",
        "longitude",
        "latitude",
        "farm.id",
        "ventilationType",
        "device_number",
        "is_running",
        "type",
        "dome",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = Controller


class OuterWaterTankAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "type",
        "ec",
        "ph",
        "do",
        "temp_in_c",
        "lph",
        "primary_membrane_filter_pressure",
        "media_filter_pressure",
        "pressure_in_atm",
        "created_at",
    ]
    list_filter = [
        "farm",
        "type",
    ]
    ordering = ["-created_at"]
    actions = ["export_selected"]

    csv_fields = [
        "id",
        "is_active",
        "created_by.id",
        "created_at",
        "farm.id",
        "longitude",
        "latitude",
        "type",
        "input_ec",
        "input_ph",
        "waste_ec",
        "waste_ph",
        "temperature",
        "primary_membrane_filter_pressure",
        "media_filter_pressure",
        "pressure",
        "waste_pressure",
        "waste_lph",
        "lph",
        "ec",
        "ph",
        "do",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = OuterWaterTank


class InnerWaterTankAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "dome",
        "recipe_name",
        "ph",
        "ec",
        "do",
        "nutrition_stage",
        "temperature_in_c",
        "water_quantity",
        # "remarks",
        "remarks_quantity",
        "created_at",
    ]
    list_filter = [
        "farm",
    ]
    ordering = ["-created_at"]
    readonly_fields = ["photo_urls"]
    actions = ["export_selected"]

    csv_fields = [
        "id",
        "is_active",
        "created_by.id",
        "created_at",
        "farm.id",
        "longitude",
        "latitude",
        "do",
        "dome",
        "ec",
        "final_ec",
        "final_ph",
        "final_temperature",
        "latitude",
        "media_filter",
        "narration",
        "new_ec",
        "new_ph",
        "new_water_quantity",
        "nutrition_stage",
        "ph",
        "ph_correction",
        "photos",
        "quantity",
        "recipe",
        "recipe_name",
        "remarks",
        "remarks_quantity",
        "temperature",
        "unit",
        "water_quantity",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = InnerWaterTank


class CoolingPadAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "ph",
        "ec",
        "tank_temperature_in_c",
        "created_at",
    ]
    list_filter = [
        "farm",
    ]
    ordering = ["-created_at"]
    actions = ["export_selected"]

    csv_fields = [
        "id",
        "is_active",
        "created_by.id",
        "created_at",
        "farm.id",
        "longitude",
        "latitude",
        "tank_temperature",
        "remarks",
        "ph",
        "ec",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = Controller


class LeafAreaDetectionAdmin(PermissionMixin, ExportCsvMixin, ImportCsvMixin):
    list_display = [
        "farm",
        "specimen",
        "leaf_area",
        "bg_area",
        "image_url_b",
        "image_url_g",
        "script_version",
        "created_by",
        "created_at",
    ]

    list_filter = [
        "farm",
        "script_version",
    ]

    csv_fields = [
        "id",
        "created_by.id",
        "created_at",
        "is_active",
        "longitude",
        "latitude",
        "farm.id",
        "leaf_area",
        "specimen.id",
        "leaf_number",
        "template_size",
        "script_version",
        "image_url_b",
        "image_url_g",
        "image_url",
        "bg_area",
        "template_length_breadth",
        "leaf_length",
        "leaf_breadth",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    ordering = ["-created_at"]
    actions = ["export_selected"]

    class Meta:
        model = LeafAreaDetection


my_admin = CustomAdminSite()

my_admin.register(NurseryHealth, NurseryHealthAdmin)
my_admin.register(VegetativeGrowth, VegetativeGrowthAdmin)
my_admin.register(ReproductiveGrowth, ReproductiveGrowthAdmin)
my_admin.register(SpecimenOutput, SpecimenOutputAdmin)
my_admin.register(Pollination, PollinationAdmin)
my_admin.register(Harvesting, HarvestingAdmin)
my_admin.register(HarvestingSample, HarvestingSampleAdmin)
my_admin.register(RootWeight, RootWeightAdmin)
my_admin.register(LeafTemperature, LeafTemperatureAdmin)
my_admin.register(RootZoneTemperature, RootZoneTemperatureAdmin)
my_admin.register(OutsideParameters, OutsideParametersAdmin)
my_admin.register(DomeParameters, DomeParametersAdmin)
my_admin.register(Controller, ControllerAdmin)
my_admin.register(OuterWaterTank, OuterWaterTankAdmin)
my_admin.register(InnerWaterTank, InnerWaterTankAdmin)
my_admin.register(CoolingPad, CoolingPadAdmin)
my_admin.register(Batch, BatchAdmin)
my_admin.register(Specimen, SpecimenAdmin)
my_admin.register(PlantAnalysis, PlantAnalysisAdmin)
my_admin.register(LeafAreaDetection, LeafAreaDetectionAdmin)
