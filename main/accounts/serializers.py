# django imports
from rest_framework import serializers

# app imports
from .models import Reimbursement


class ReimbursementSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data["created_by"] = self.context["request"].user
        return validated_data

    class Meta:
        model = Reimbursement
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
        }
