import datetime
import csv
import codecs
import json
import re
import logging


# django imports
from django.contrib import admin, messages
from django.http.response import HttpResponseRedirect
from django import forms
from django.shortcuts import render


# project imports
from users.models import User
from farms.models import Farm
from pdc.models import Batch, Specimen
from labour.models import Labour
from libs.helpers import csv_dispatcher


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ExportCsvMixin:
    model = ""
    csv_fields = list()

    def get_repr(self, value):
        if value is None:
            return "-"
        if isinstance(value, list):
            if value == []:
                value = ""
            if isinstance(value[0], str):
                value = ", ".join(value)

            elif isinstance(value[0], dict):
                value = json.dumps(value)
                value = value.replace(",", "|")

        elif isinstance(value, str) and "," in value:
            value = value.replace("|", ",")
        elif isinstance(value, (datetime.date, datetime.time, int, float)):
            return str(value)
        elif callable(value):
            return "%s" % value()
        return value

    def get_field(self, instance, field):
        field_path = field.split(".")
        attr = instance
        for elem in field_path:
            try:
                attr = getattr(attr, elem)
            except AttributeError:
                return None
        return attr

    def export_selected(self, request, queryset=None):
        # exports fields sent from admin
        fields = self.csv_fields
        csv = ""
        csv += ",".join(self.csv_fields) + "\n"
        if queryset is None:
            queryset = self.model.objects.all()
        for obj in queryset:
            row = [self.get_repr(self.get_field(obj, field)) for field in fields]
            csv += ",".join(str(v) for v in row) + "\n"
        return csv_dispatcher(csv)


class ImportCsvMixin:
    def import_csv(self, request):
        model = self.model
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = csv.reader(codecs.iterdecode(csv_file, "utf-8"))
            header = next(reader)
            added, invalid = 0, 0
            for row in reader:
                try:
                    _object_dict = {key: value for key, value in zip(header, row)}

                    created_by = User.objects.get(id=_object_dict["created_by.id"])
                    farm = Farm.objects.get(id=_object_dict["farm.id"])

                    _object_dict.update({"created_by": created_by, "farm": farm})

                    dict = {k: v for k, v in _object_dict.items() if v != "-"}

                    # storing all the foregin key in a set

                    foreign_keys = set()
                    for i in dict:
                        if re.search(".id$", i):
                            foreign_keys.add(i)

                    # getting user by id
                    if "decommission_by.id" in foreign_keys:
                        decommission_by = User.objects.get(
                            id=_object_dict["decommission_by.id"]
                        )
                        dict["decommission_by"] = decommission_by
                        dict.pop("decommission_by.id")

                    # getting batch by id
                    if "batch.id" in foreign_keys:
                        batch = Batch.objects.get(id=_object_dict["batch.id"])
                        dict["batch"] = batch
                        dict.pop("batch.id")

                    # getting farm by id
                    if "commercial_farm.id" in foreign_keys:
                        commercial_farm = Farm.objects.get(
                            id=_object_dict["commercial_farm.id"]
                        )
                        dict["commercial_farm"] = commercial_farm
                        dict.pop("commercial_farm.id")

                    # getting specimen by id
                    if "specimen.id" in foreign_keys:
                        specimen = Specimen.objects.get(id=_object_dict["specimen.id"])
                        dict["specimen"] = specimen
                        dict.pop("specimen.id")

                    # getting labour by id
                    if "labour.id" in foreign_keys:
                        labour = Labour.objects.get(id=_object_dict["labour.id"])
                        dict["labour"] = labour
                        dict.pop("labour.id")

                    # json loading of recipe
                    if "recipe" in dict.keys():
                        unformatted_recipe = dict["recipe"].replace("|", ",")
                        dict["recipe"] = json.loads(unformatted_recipe)

                    if "remarks" in dict.keys():
                        dict["remarks"] = [dict["remarks"]]

                    """keys = [
                        "created_by.id",
                        "farm.id",
                        "id",
                        "specimen.id",
                        "batch.id",
                        "labour.id",
                        "decommission_by.id",
                        "commercial_farm.id",
                    ]"""
                    # removing unwanted keys

                    final_dict = {
                        key: dict[key] for key in dict if key not in foreign_keys
                    }

                    model.objects.create(**final_dict)
                    # model.objects.create(**dict)
                    added += 1
                except Exception:
                    logging.logger.info("", exc_info=True)
                    invalid += 1
            messages.success(
                request, f"Csv Imported, Added - {added} , Invalid - {invalid}"
            )
            return HttpResponseRedirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)


class PermissionMixin(admin.ModelAdmin):
    show_full_result_count = False

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name="PDC | Edit Access").exists():
            return True
        else:
            return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name="PDC | Delete Access").exists():
            return True
        else:
            return False

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if hasattr(obj, "created_by") and "created_by" not in readonly_fields:
            readonly_fields.append("created_by")
        return readonly_fields


class BaseMixin(admin.ModelAdmin):
    show_full_result_count = False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
        if hasattr(obj, "created_by") and "created_by" not in readonly_fields:
            readonly_fields.append("created_by")
        return readonly_fields
