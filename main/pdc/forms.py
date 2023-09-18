from django import forms
from datetime import datetime


class ChangeBatchStatus(forms.Form):
    is_active = forms.BooleanField(required=False)
    remarks = forms.CharField(max_length=255)
    decommission_date = forms.DateField(
        initial=datetime.now().date, label="Date to decommision (YYYY-MM-DD)"
    )


class ChangeSpecimenStatus(forms.Form):
    is_active = forms.BooleanField(required=False)
    remarks = forms.CharField(max_length=255)
    decommission_date = forms.DateField(
        initial=datetime.now().date, label="Date to decommision (YYYY-MM-DD)"
    )
