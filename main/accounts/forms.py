from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _

# app imports
from .models import Reimbursement


class ChangeReimbursementStatus(forms.Form):

    remarks = forms.CharField(max_length=255)
    status = forms.ChoiceField(choices=Reimbursement.Status.choices)
