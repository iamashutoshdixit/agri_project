# project imports
from libs.mixins import BaseMixin, PermissionMixin, ExportCsvMixin, ImportCsvMixin
from pdc.admin import my_admin
from django.urls import path

# app imports
from .models import Labour, Work, Attendance

# Register your models here.


class WorkAdmin(PermissionMixin, ImportCsvMixin, ExportCsvMixin):
    list_display = [
        "farm",
        "labour",
        "duration",
        "type",
        "recipe",
        "recipe_quantity",
        "water_quantity",
        "dome",
        "description",
        "work_quantity",
        "created_at",
        "created_by",
    ]
    list_filter = [
        "farm",
    ]
    date_hierarchy = "created_at"
    readonly_fields = ["created_by"]
    actions = ["change_status", "export_selected"]
    csv_fields = [
        "farm.name",
        "farm.id",
        "labour.name",
        "labour.id",
        "duration",
        "description",
        "type",
        "work_quantity",
        "recipe_quantity",
        "water_quantity",
        "dome",
        "remarks",
        "recipe",
        "created_by.id",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = Work


class AttendanceAdmin(PermissionMixin, ImportCsvMixin, ExportCsvMixin):
    list_display = [
        "farm",
        "labour",
        "action",
        "datetime",
        "created_at",
        "created_by",
    ]
    list_filter = [
        "farm",
    ]
    date_hierarchy = "created_at"
    readonly_fields = ["created_by"]
    actions = ["change_status", "export_selected"]

    csv_fields = [
        "labour",
        "datetime",
        "farm",
        "action",
        "farm.id",
        "created_by.id",
        "created_by",
        "labour.id",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    class Meta:
        model = Attendance


class LabourAdmin(BaseMixin):
    list_display = [
        "id",
        "name",
        "mobile",
        "kyc_number",
        "created_at",
        "created_by",
        "updated_at",
    ]
    readonly_fields = ["kyc_images", "created_by"]
    list_filter = ["farms"]


my_admin.register(Labour, LabourAdmin)
my_admin.register(Attendance, AttendanceAdmin)
my_admin.register(Work, WorkAdmin)
