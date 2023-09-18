# django imports
from django import forms

# app imports
from .models import IssueTracker
from .helpers import get_issue_tracker_status


class IssueTrackerForm(forms.ModelForm):
    status = forms.ChoiceField(choices=get_issue_tracker_status)

    class Meta:
        model = IssueTracker
        fields = "__all__"
