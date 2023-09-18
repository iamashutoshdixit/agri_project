# django imports
from django.core.exceptions import ValidationError
from rest_framework import serializers

# project imports
from farms.models import Farm


# app imports
from . import models


class BaseSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data["created_by"] = self.context["request"].user
        return validated_data


class SpecimenSerializer(BaseSerializer):
    class Meta:
        model = models.Specimen
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
        }


class BatchSerializer(BaseSerializer):
    class Meta:
        model = models.Batch
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
        }

    def validate_farm(self, farm):
        if farm.type == Farm.FarmType.NURSERY:
            return farm
        raise ValidationError("Farm should be a Nursery")

    def validate_commercial_farm(self, farm):
        if farm.type == Farm.FarmType.COMMERCIAL:
            return farm
        raise ValidationError("This farm should be a commercial farm")

    def validate(self, kwargs):
        instance = models.Batch(**kwargs)
        instance.clean()
        return super().validate(kwargs)


class PlantAnalysisSerializer(BaseSerializer):
    class Meta:
        model = models.PlantAnalysis
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
            "batch": {
                "error_messages": {
                    "does_not_exist": "Batch does not exist",
                }
            },
        }


class NurseryHealthSerializer(BaseSerializer):
    class Meta:
        model = models.NurseryHealth
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
            "specimen": {
                "error_messages": {
                    "does_not_exist": "Specimen does not exist",
                }
            },
        }


class VegetativeGrowthSerializer(BaseSerializer):
    class Meta:
        model = models.VegetativeGrowth
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
            "specimen": {
                "error_messages": {
                    "does_not_exist": "Specimen does not exist",
                }
            },
        }


class ReproductiveGrowthSerializer(BaseSerializer):
    class Meta:
        model = models.ReproductiveGrowth
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
            "specimen": {
                "error_messages": {
                    "does_not_exist": "Specimen does not exist",
                }
            },
        }


class SpecimenOutputSerializer(BaseSerializer):
    class Meta:
        model = models.SpecimenOutput
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
            "specimen": {
                "error_messages": {
                    "does_not_exist": "Specimen does not exist",
                }
            },
        }


class PollinationSerializer(BaseSerializer):
    class Meta:
        model = models.Pollination
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
        }


class HarvestingSerializer(BaseSerializer):
    class Meta:
        model = models.Harvesting
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
        }


class HarvestingSampleSerializer(BaseSerializer):
    class Meta:
        model = models.HarvestingSample
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
        }


class RootWeightSerializer(BaseSerializer):
    class Meta:
        model = models.RootWeight
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
        }


class LeafTemperatureSerializer(BaseSerializer):
    class Meta:
        model = models.LeafTemperature
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
        }


class RootZoneTemperatureSerializer(BaseSerializer):
    class Meta:
        model = models.RootZoneTemperature
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
        }


class OutsideParametersSerializer(BaseSerializer):
    class Meta:
        model = models.OutsideParameters
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
        }


class DomeParametersSerializer(BaseSerializer):
    class Meta:
        model = models.DomeParameters
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
        }


class ControllerSerializer(BaseSerializer):
    class Meta:
        model = models.Controller
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
        }


class OuterWaterTankSerializer(BaseSerializer):
    class Meta:
        model = models.OuterWaterTank
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
        }


class InnerWaterTankSerializer(BaseSerializer):
    class Meta:
        model = models.InnerWaterTank
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
        }


class CoolingPadSerializer(BaseSerializer):
    class Meta:
        model = models.CoolingPad
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
        }


class LeafAreaDetectionSerializer(BaseSerializer):
    class Meta:
        model = models.LeafAreaDetection
        fields = "__all__"
        extra_kwargs = {
            "farm": {
                "error_messages": {
                    "does_not_exist": "Farm does not exist",
                }
            },
        }
