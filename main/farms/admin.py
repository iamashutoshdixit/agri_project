# project imports
from libs.mixins import BaseMixin
from pdc.admin import my_admin

# app imports
from .models import (
    Camera,
    Farm,
    FarmManagerAttendance,
    IOTBox,
    IssueTracker,
    VisitorEntry,
)
from .forms import IssueTrackerForm
from .helpers import get_issue_tracker_status


class FarmManagerAttendanceAdmin(BaseMixin):
    list_display = [
        "farm",
        "user",
        "action",
        "created_at",
    ]
    list_filter = [
        "farm",
    ]
    date_hierarchy = "created_at"


class VisitorEntryAdmin(BaseMixin):
    list_display = (
        "datetime",
        "name",
        "address",
        "mobile_number",
        "purpose_of_visit",
        "feedback",
        "created_at",
    )
    date_hierarchy = "created_at"


class IssueTrackerAdmin(BaseMixin):
    list_display = (
        "farm",
        "component",
        "issue",
        "issue_status",
        "actions",
        "assignee",
        "priority",
        "datetime",
        "created_at",
        "created_by",
        "updated_at",
    )
    list_filter = [
        "farm",
    ]
    readonly_fields = ["created_at", "updated_at", "photo_urls", "created_by"]
    form = IssueTrackerForm

    def issue_status(self, obj=None):
        if obj is None:
            return ""
        st = obj.status
        statuses = get_issue_tracker_status()
        status = list(filter(lambda x: str(x[0]) == str(st), statuses))[0][1]
        return status

    issue_status.short_description = "Status"

    def save_model(self, request, obj, form, change):
        if obj.id is None:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class FarmAdmin(BaseMixin):
    list_display = (
        "id",
        "farm_code",
        "type",
        "name",
        "area",
        "city",
        "state",
        "cameras",
        "created_at",
        "updated_at",
        "is_active",
    )
    list_filter = [
        "state",
        "type",
    ]
    readonly_fields = ["created_at", "updated_at"]

    def save_model(self, request, obj, form, change):
        if obj.id is None:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class CameraAdmin(BaseMixin):
    list_display = (
        "farm",
        "name",
        "channel",
        "created_at",
        "updated_at",
    )
    readonly_fields = ["created_at", "updated_at", "video"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 0:
            return qs
        else:
            return qs.filter(farm__in=request.user.farms.all())

    def save_model(self, request, obj, form, change):
        if obj.id is None:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class IOTBoxAdmin(BaseMixin):
    list_display = (
        "id",
        "serial_number",
        "farm_name",
        "uuid",
        "params",
        "created_at",
        "updated_at",
        "is_active",
    )
    readonly_fields = ["created_at", "updated_at", "farm"]

    def save_model(self, request, obj, form, change):
        if obj.id is None:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


my_admin.disable_action("delete_selected")
my_admin.register(Farm, FarmAdmin)
my_admin.register(Camera, CameraAdmin)
my_admin.register(IOTBox, IOTBoxAdmin)
my_admin.register(VisitorEntry, VisitorEntryAdmin)
my_admin.register(IssueTracker, IssueTrackerAdmin)
my_admin.register(FarmManagerAttendance, FarmManagerAttendanceAdmin)
