# python imports

# django imports
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# project imports
from libs.mixins import BaseMixin
from pdc.admin import my_admin

# app imports
from .models import Reimbursement
from .forms import ChangeReimbursementStatus


class ReimbursementAdmin(BaseMixin):
    list_display = (
        "id",
        "invoice_date",
        "invoice_no",
        "amount",
        "status",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    )
    actions = ["change_status"]
    readonly_fields = ["items_list", "photo_urls", "created_at", "updated_at"]
    exclude = ["items", "photos"]
    list_filter = ["status"]
    search_fields = ["invoice_no", "created_by__username"]
    date_hierarchy = "created_at"

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    # status cannot be changed if status is not OPEN
    def change_status(self, request, queryset):
        if "set_reimbursement_status" in request.POST:
            form = ChangeReimbursementStatus(request.POST)
            if form.is_valid():
                remarks = form.cleaned_data["remarks"]
                status = form.cleaned_data["status"]
                obj = queryset.first()
                obj.updated_by = request.user
                obj.remarks = remarks
                obj.status = status
                obj.save()
                return HttpResponseRedirect(".")
        else:
            form = ChangeReimbursementStatus()
            if len(queryset) > 1:
                return HttpResponse("please select one item at a time")
            if queryset.last().status != Reimbursement.Status.OPEN.value:
                return HttpResponse("Status is already updated")
        context = {
            "title": "Change status of Reimbursement",
            "objects": queryset,
            "form": form,
        }
        return render(request, "accounts/reimbursement/change-status.html", context)


my_admin.register(Reimbursement, ReimbursementAdmin)
