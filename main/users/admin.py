# django imports
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin

# project imports
from libs.mixins import BaseMixin
from pdc.admin import my_admin

# app imports
from .models import User


class LabourAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "mobile",
        "aadhar_number",
    ]


class UserAdmin(UserAdmin, BaseMixin):
    show_full_result_ount = False
    fieldsets = ()
    fields = (
        "username",
        "password",
        "role",
        "first_name",
        "last_name",
        "farms",
        "is_active",
        "groups",
        "user_permissions",
    )
    list_display = ["username", "first_name", "last_name", "role", "is_staff"]
    list_filter = ["is_active", "role"]

    def has_delete_permission(self, request, obj=None):
        return False

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.add_farm_in_group_to_user()


my_admin.register(User, UserAdmin)
my_admin.register(Group)
my_admin.register(Permission)
