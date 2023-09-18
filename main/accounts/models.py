# python imports

# django imports
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

# user inports
from libs.models import BaseTemplateWithActor
from users.models import User

# Create your models here.


class Reimbursement(BaseTemplateWithActor):
    """
    Model to store Reimbursement data
    """

    class Status(models.IntegerChoices):
        OPEN = 0, _("Open")
        REJECTED = 1, _("Rejected")
        APPROVED = 2, _("Approved")

    is_active = None
    invoice_date = models.DateTimeField()
    invoice_no = models.IntegerField()
    items = models.JSONField()
    amount = models.IntegerField()
    photos = ArrayField(models.URLField(), null=True, blank=True)
    status = models.IntegerField(
        choices=Status.choices, null=False, default=Status.OPEN
    )

    # form
    remarks = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.ForeignKey(
        "users.User",
        related_name="reimbursement_approved_by",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    @property
    def photo_urls(self):
        tag = ""
        if self.photos is None:
            return mark_safe(f"{tag}")
        for url in self.photos:
            tag += f"""
            <div style="margin-bottom: 1em">
                <img style="width: 30%; height: 30%" src="{url}"/>
            </div>
            """
        return mark_safe(f"{tag}")

    def items_list(self):
        tag = ""
        if self.items is None:
            return mark_safe(f"{tag}")
        for i in self.items:
            tag += f"""
            <div style="margin-bottom: 1em">
                <h3>Title: <span>{i["title"]}</span> </h3>
                <h3>Description: <span>{i["description"]}</span></h3>
                <h3>Cost: <span>{i["cost"]}</span></h3>
            </div>
            """
        return mark_safe(f"{tag}")

    class Meta:
        verbose_name = "Reimbursements"
        verbose_name_plural = "Reimbursements"
