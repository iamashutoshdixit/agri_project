# python imports
from datetime import datetime

# django imports
from django.core.exceptions import ValidationError
from rest_framework import serializers

# app imports
from .models import (
    Farm,
    VisitorEntry,
    IssueTracker,
    Camera,
    IOTBox,
    FarmManagerAttendance,
)


class VisitorEntrySerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = VisitorEntry
        fields = "__all__"


class IssueTrackerSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = IssueTracker
        fields = "__all__"


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = "__all__"


class IOTBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = IOTBox
        fields = "__all__"


class FarmManagerAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmManagerAttendance
        fields = "__all__"
        extra_kwargs = {
            "user": {
                "error_messages": {
                    "does_not_exist": "User does not exist.",
                }
            }
        }

    def validate(self, attrs):
        user = attrs["user"]
        action = attrs["action"]
        farm = attrs["farm"]

        qs = FarmManagerAttendance.objects.filter(
            farm=farm,
            user=user,
            created_at__date=datetime.now().date(),
        )
        qs_pi = qs.filter(action=0)
        qs_po = qs.filter(action=1)

        # let farm managers punch in and out multiple times
        # if action == 0:
        #     if len(qs_pi) > 0:
        #         raise ValidationError(
        #             {"errors": "User has already punched in."},
        #         )

        if action == 1:
            if len(qs_pi) == 0:
                raise ValidationError(
                    {"errors": "User hasn't punched in yet."},
                )
            if len(qs_po) > 0:
                raise ValidationError(
                    {"errors": "User has already punched out."},
                )

        return super().validate(attrs)


class FarmSerializer(serializers.ModelSerializer):
    iotbox = IOTBoxSerializer()

    class Meta:
        model = Farm
        fields = "__all__"
