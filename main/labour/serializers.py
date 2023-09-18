# python imports
from datetime import datetime
from cerberus import Validator

# django imports
from django.core.exceptions import ValidationError
from rest_framework import serializers

# user imports
from . import models


class LabourSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Labour
        exclude = ["is_staff", "user_id"]

    def validate(self, attrs):
        data = attrs
        farms = []
        if "farms" in data:
            farms = data.pop("farms")
        instance = models.Labour(**data)
        instance.clean()
        data["farms"] = farms
        return data


class WorkSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Work
        fields = "__all__"

    def validate_recipe(self, val):
        if not isinstance(val, list):
            raise ValidationError("expected list of objects")
        if len(val) == 0:
            raise ValidationError("this field cannot be empty.")
        schema = {
            "chemical": {"type": "string"},
            "amount": {"type": "integer"},
            "unit": {"type": "string"},
        }
        v = Validator(schema)
        v.require_all = True
        for recipe in val:
            valid = v.validate(recipe)
            if not valid:
                raise ValidationError(v.errors)
        return val


class AttendanceSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Attendance
        fields = "__all__"
        extra_kwargs = {
            "labour": {
                "error_messages": {
                    "does_not_exist": "labour {pk_value} does not exist"
                },
            }
        }

    def validate(self, attrs):
        """
        validate sent labour attendance
        """
        labour = attrs["labour"]
        action = attrs["action"]
        farm = attrs["farm"]
        dt = self.initial_data["datetime"]

        qs = models.Attendance.objects.filter(
            labour=labour,
            datetime__date=datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ").date(),
            farm=farm,
        )
        qs_pi = qs.filter(action=0)
        qs_po = qs.filter(action=1)

        if action == 0:
            if len(qs_pi) > len(qs_po):
                raise ValidationError(
                    {
                        "errors": "Labour has already punched in.",
                    }
                )

        if action == 1:
            if len(qs_pi) == len(qs_po):
                raise ValidationError(
                    {
                        "errors": "Labour hasn't punched in yet.",
                    }
                )

        # let labours punch in and out multiple times in a day
        # if action == 2:
        #     if qs_pi or qs_po:
        #         raise ValidationError(
        #             {"errors": "Labour has already marked their attendance."}
        #         )

        return attrs
