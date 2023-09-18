# django imports
from rest_framework import serializers

# user imports
from .models import User
from farms.serializers import FarmSerializer


class UserSerializer(serializers.ModelSerializer):
    farms = FarmSerializer(many=True)

    class Meta:
        model = User
        # fields = "__all__"
        exclude = (
            "is_active",
            "created_at",
            "updated_at",
            "password",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
        )
