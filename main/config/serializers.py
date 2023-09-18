# django imports
from rest_framework import serializers

# app imports
from .models import Config


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = "__all__"
