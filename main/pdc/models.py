# python imports

import uuid
from datetime import datetime as dt

# django imports

from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.html import mark_safe

# user imports

from farms.models import Farm
from libs.models import BaseTemplate
from users.models import User


# CONSTANTS/TAGS
def generate_id():
    """
    Generate uuid, convert to hex, take first 6 characters,
    convert to upper and return
    """
    uid = uuid.uuid4().hex[:6].upper()
    while Batch.objects.filter(pk=uid):
        uid = uuid.uuid4().hex[:6].upper()
    return uuid.uuid4().hex[:6].upper()


class BaseModel(BaseTemplate):
    """
    Base model for models in this module to inherit from
    """

    created_at = models.DateTimeField(default=dt.now)
    farm = models.ForeignKey(Farm, on_delete=models.PROTECT)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True
    )
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    class Meta:
        abstract = True


class Specimen(BaseModel):
    """
    Model to store specimen details
    """

    farm = models.ForeignKey(Farm, on_delete=models.PROTECT)
    id = models.CharField(
        max_length=6, default=generate_id, primary_key=True, editable=False
    )
    batch = models.ForeignKey("Batch", on_delete=models.PROTECT, null=True)
    position = models.IntegerField()
    chamber = models.IntegerField()
    line = models.IntegerField()
    set = models.IntegerField()
    dome = models.IntegerField()
    remarks = models.CharField(max_length=255, null=True, blank=True)
    decommission_date = models.DateField(null=True, blank=True)
    decommission_by = models.ForeignKey(
        "users.User",
        related_name="specimen_decommission_by",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Specimen"
        verbose_name_plural = "Specimen"

    def __str__(self):
        return f"{self.id}"


class Batch(BaseModel):
    """
    Model to store details for a particular batch
    """

    farm = models.ForeignKey(Farm, on_delete=models.PROTECT)
    id = models.CharField(
        max_length=6,
        primary_key=True,
        default=generate_id,
        editable=False,
    )

    # Nursery specific
    crop_name = models.CharField(max_length=20)
    variety = models.CharField(max_length=20)
    sowing_date = models.DateField()
    no_of_seeds = models.IntegerField()

    # Commercial specific
    commercial_farm = models.ForeignKey(
        Farm,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="commercial_farm",
    )
    dome = models.IntegerField(null=True, blank=True)
    transplantation_date = models.DateField(null=True, blank=True)
    no_of_plants = models.IntegerField(null=True, blank=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    decommission_date = models.DateField(null=True, blank=True)
    decommission_by = models.ForeignKey(
        "users.User",
        related_name="batch_decommission_by",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def clean(self):
        errors = {}

        # nursery farm checks
        if self.farm.type == Farm.FarmType.NURSERY:
            non_fields = [
                "commercial_farm",
                "dome",
                "transplantation_date",
                "no_of_plants",
            ]
            for field in non_fields:
                if getattr(self, field):
                    message = f"Cannot specify {field} for nursery batch."
                    errors[field] = message

        # commercial farm checks
        if self.farm.type == Farm.FarmType.COMMERCIAL:
            pass

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Batch"
        verbose_name_plural = "Batches"


class PlantAnalysis(BaseModel):
    """
    Model to store plant analysis data
    """

    farm = models.ForeignKey(Farm, on_delete=models.PROTECT)
    id = models.CharField(
        max_length=6, primary_key=True, default=generate_id, editable=False
    )
    specimen = models.ForeignKey(
        Specimen, on_delete=models.PROTECT, null=True, blank=True
    )
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT)
    line = models.IntegerField()
    dome = models.IntegerField()
    section = models.IntegerField()
    photos = ArrayField(models.URLField(), null=True, blank=True)

    type = models.CharField(max_length=30)
    category = models.CharField(max_length=50)
    remarks = ArrayField(models.CharField(max_length=50))
    comments = models.CharField(max_length=100)

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

    class Meta:
        verbose_name = "Plant Analysis"
        verbose_name_plural = "Plant Analysis"
        ordering = ["-created_at"]


class NurseryHealth(BaseModel):
    """
    Model to store nursery health data
    """

    specimen = models.ForeignKey(Specimen, on_delete=models.PROTECT)
    germination = models.DecimalField(
        max_digits=4,
        decimal_places=2,
    )
    plant_height = models.FloatField()
    nodes = models.IntegerField()
    remarks = ArrayField(models.CharField(max_length=50))
    observation = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    photo = ArrayField(models.URLField(), null=True, blank=True)

    @property
    def photo_urls(self):
        tag = ""
        if self.photo is None:
            return mark_safe(f"{tag}")
        for url in self.photo:
            tag += f"""
            <div style="margin-bottom: 1em">
                <img style="width: 30%; height: 30%" src="{url}"/>
            </div>
            """
        return mark_safe(f"{tag}")

    class Meta:
        verbose_name = "Nursery Health"
        verbose_name_plural = "Nursery Health"


class VegetativeGrowth(BaseModel):
    """
    Model to store data on vegetative growth
    """

    specimen = models.ForeignKey(Specimen, on_delete=models.PROTECT)
    stem = models.IntegerField(
        choices=[
            (1, "A"),
            (2, "B"),
        ],
        null=True,
        blank=True,
    )
    plant_height = models.FloatField()
    stem_diameter = models.FloatField()
    stem_diameter_2 = models.FloatField(null=True, blank=True)
    no_of_branches = models.IntegerField(null=True, blank=True)
    no_of_branch_nodes = models.IntegerField()
    internode_distance = models.FloatField(null=True, blank=True)
    nodes = models.IntegerField(null=True, blank=True)
    fruit_distance = models.FloatField(null=True, blank=True)
    no_of_petioles = models.IntegerField(null=True, blank=True)
    length_of_petioles = models.FloatField(null=True, blank=True)
    leaves_in_petioles = models.IntegerField(null=True, blank=True)
    photo = ArrayField(models.URLField(), null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=50, null=True, blank=True)

    @property
    def photo_urls(self):
        tag = ""
        if self.photo is None:
            return mark_safe(f"{tag}")
        for url in self.photo:
            tag += f"""
            <div style="margin-bottom: 1em">
                <img style="width: 30%; height: 30%" src="{url}"/>
            </div>
            """
        return mark_safe(f"{tag}")

    def clean(self):
        if not self.farm:
            return
        if self.farm.type == Farm.FarmType.COMMERCIAL:
            non_fields = [
                "no_of_branches",
                "fruit_distance",
                "no_of_petioles",
                "length_of_petioles",
                "leaves_in_petioles",
            ]
            for field in non_fields:
                if getattr(self, field):
                    raise ValidationError(
                        {field: "this field is not for commercial farm"}
                    )
        raise ValidationError("")

    class Meta:
        verbose_name = "Vegetative Growth"
        verbose_name_plural = "Vegetative Growth"


class ReproductiveGrowth(BaseModel):
    """
    Model to store plant flowering data
    """

    specimen = models.ForeignKey(Specimen, on_delete=models.PROTECT)
    remarks = models.CharField(max_length=50, null=True, blank=True)
    cluster = models.IntegerField()
    flowering = models.JSONField()
    stem = models.IntegerField(
        choices=[
            (1, "A"),
            (2, "B"),
        ],
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Reproductive Growth"
        verbose_name_plural = "Reproductive Growth"


class SpecimenOutput(BaseModel):
    """
    Model to record specimen output
    """

    specimen = models.ForeignKey(Specimen, on_delete=models.PROTECT)
    harvested_fruits = models.IntegerField()
    harvested_weight = models.IntegerField()
    stage_of_harvest = models.CharField(max_length=50, default="")

    class Meta:
        verbose_name = "Specimen Output"
        verbose_name_plural = "Specimen Output"


class LeafAreaDetection(BaseModel):
    """
    Model to store LAD output
    """

    specimen = models.ForeignKey(Specimen, on_delete=models.PROTECT, null=True)
    leaf_number = models.IntegerField()
    image_url_b = models.CharField(max_length=128)
    image_url_g = models.CharField(max_length=128)
    image_url = models.CharField(max_length=128)
    bg_area = models.FloatField()
    leaf_area = models.FloatField()
    leaf_length = models.FloatField(null=True)
    leaf_breadth = models.FloatField(null=True)
    template_length_breadth = models.CharField(max_length=10, null=True)
    template_size = models.IntegerField()
    script_version = models.CharField(max_length=3)

    class Meta:
        verbose_name = "LeafAreaDetection"
        verbose_name_plural = "LeafAreaDetection"


class Pollination(BaseModel):
    """
    Model to store dome wise pollination data
    """

    dome = models.IntegerField()
    batch = models.ForeignKey(
        Batch,
        on_delete=models.PROTECT,
        null=True,
    )
    line = models.IntegerField()
    section = models.CharField(
        max_length=1,
        null=True,
        blank=True,
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    count = models.IntegerField()

    class Meta:
        verbose_name = "Pollination"
        verbose_name_plural = "Pollination"

    @property
    def total(self):
        return self.morning + self.evening


class Harvesting(BaseModel):
    """
    model to store dome wise harvesting data
    """

    dome = models.IntegerField()
    batch = models.ForeignKey(
        Batch,
        on_delete=models.PROTECT,
        null=True,
    )
    line = models.IntegerField()
    variety = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    total_weight = models.FloatField()
    photo = ArrayField(models.URLField(), null=True, blank=True)
    brix_value = models.FloatField(null=True, blank=True)
    pure_weight = models.FloatField()
    wastage_weight = models.FloatField()
    remarks = models.CharField(max_length=255, null=True, blank=True)
    average_weight = models.FloatField(null=True, blank=True)

    @property
    def photo_urls(self):
        tag = ""
        if self.photo is None:
            return mark_safe(f"{tag}")
        for url in self.photo:
            tag += f"""
            <div style="margin-bottom: 1em">
                <img style="width: 30%; height: 30%" src="{url}"/>
            </div>
            """
        return mark_safe(f"{tag}")

    class Meta:
        verbose_name = "Harvesting"
        verbose_name_plural = "Harvesting"


class HarvestingSample(BaseModel):
    dome = models.IntegerField()
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT)
    no_of_fruits = models.IntegerField()
    weight_of_fruits = models.FloatField()
    brix_value = models.FloatField()
    fruit_color = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Harvesting Sample"
        verbose_name_plural = "Harvesting Samples"


class RootWeight(BaseModel):
    """
    Model to store root weight dome wise
    """

    dome = models.IntegerField()
    batch = models.ForeignKey(
        Batch,
        on_delete=models.PROTECT,
        null=True,
    )
    line = models.IntegerField()
    section = models.CharField(
        max_length=1,
        null=True,
        blank=True,
    )
    type = models.IntegerField(
        choices=[
            (1, "Dry"),
            (2, "Wet"),
        ],
        default=1,
    )
    weight = models.FloatField()

    class Meta:
        verbose_name = "Root Weight"
        verbose_name_plural = "Root Weight"


class LeafTemperature(BaseModel):
    """
    Model to record leaf temperature
    """

    dome = models.IntegerField()
    batch = models.ForeignKey(
        Batch,
        on_delete=models.PROTECT,
        null=True,
    )
    line = models.IntegerField()
    section = models.CharField(
        max_length=1,
        null=True,
        blank=True,
    )
    temperature = models.FloatField()

    class Meta:
        verbose_name = "Leaf Temperature"
        verbose_name_plural = "Leaf Temperature"

    @property
    def avg_temp(self):
        return f"{self.t1 + self.t2 + self.t3 + self.t4 + self.t5 / 5} °C"


class RootZoneTemperature(BaseModel):
    """
    Model to store root zone temperatures
    """

    dome = models.IntegerField()
    batch = models.ForeignKey(
        Batch,
        on_delete=models.PROTECT,
        null=True,
    )
    line = models.IntegerField()
    section = models.CharField(
        max_length=1,
        null=True,
        blank=True,
    )
    water_temperature = models.FloatField()
    surface_temperature = models.FloatField(null=True, blank=True)

    @property
    def water_temperature_in_c(self):
        return f"{self.water_temperature} °C"

    @property
    def surface_temperature_in_c(self):
        return f"{self.surface_temperature} °C"

    class Meta:
        verbose_name = "Root Zone Temperature"
        verbose_name_plural = "Root Zone Temperature"


class OutsideParameters(BaseModel):
    """
    Model to store outside climatic parameters
    """

    weather = models.CharField(max_length=50)
    wind_speed = models.FloatField()
    wind_direction = models.CharField(max_length=50)
    temperature = models.FloatField()
    humidity = models.FloatField()
    lux = models.FloatField(null=True, blank=True)

    @property
    def temperature_in_c(self):
        return f"{self.temperature} °C"

    @property
    def wind_speed_in_km_hr(self):
        return f"{self.wind_speed}  km/hr"

    @property
    def humidity_in_p(self):
        return f"{self.humidity}%"

    @property
    def lux_in_lux(self):
        return f"{self.lux} Lux"

    class Meta:
        verbose_name = "Outside Parameters"
        verbose_name_plural = "Outside Parameters"


class DomeParameters(BaseModel):
    """
    Model to store dome parameters
    """

    dome = models.IntegerField()
    temperature = models.FloatField()
    dry_temperature = models.FloatField()
    wet_temperature = models.FloatField()
    humidity = models.FloatField()
    lux = models.FloatField(null=True, blank=True)
    par_meter = models.FloatField(null=True, blank=True)

    @property
    def temperature_in_c(self):
        return f"{self.temperature} °C"

    @property
    def dry_temperature_in_c(self):
        return f"{self.dry_temperature} °C"

    @property
    def wet_temperature_in_c(self):
        return f"{self.wet_temperature} °C"

    @property
    def humidity_in_p(self):
        return f"{self.humidity}%"

    @property
    def lux_in_lux(self):
        return f"{self.lux} Lux"

    class Meta:
        verbose_name = "Dome Parameters"
        verbose_name_plural = "Dome Parameters"


class Controller(BaseModel):
    """
    Model to store details on exhaust, vents, cooling pad or shade net
    """

    dome = models.IntegerField()
    ventilationType = models.IntegerField(default=1)
    type = models.IntegerField(default=1)
    device_number = models.IntegerField(null=True, blank=True)
    is_running = models.BooleanField()

    class Meta:
        verbose_name = "Climate Controller"
        verbose_name_plural = "Climate Controller"


class OuterWaterTank(BaseModel):
    """
    Model to store data on water tanks (outer)
    """

    type = models.IntegerField(
        choices=[
            (1, "RO"),
            (2, "RW"),
        ],
    )
    input_ec = models.FloatField(null=True, blank=True)
    input_ph = models.FloatField(null=True, blank=True)
    ec = models.FloatField()
    ph = models.FloatField()
    waste_ec = models.FloatField(null=True, blank=True)
    waste_ph = models.FloatField(null=True, blank=True)
    do = models.FloatField(null=True, blank=True)
    temperature = models.FloatField()
    lph = models.FloatField()
    waste_lph = models.FloatField(null=True, blank=True)
    primary_membrane_filter_pressure = models.FloatField(null=True, blank=True)
    media_filter_pressure = models.FloatField()
    pressure = models.FloatField(null=True, blank=True)
    waste_pressure = models.FloatField(null=True, blank=True)

    @property
    def temp_in_c(self):
        return f"{self.temperature} °C"

    @property
    def pressure_in_atm(self):
        return f"{self.pressure} atm"

    class Meta:
        verbose_name = "Outer Water Tank"
        verbose_name_plural = "Outer Water Tank"


class InnerWaterTank(BaseModel):
    """
    Model to store data on water tanks (inner)
    """

    dome = models.IntegerField()
    recipe_name = models.CharField(max_length=20)
    ph = models.FloatField()
    ec = models.FloatField()
    new_ec = models.FloatField(null=True, blank=True)
    new_ph = models.FloatField(null=True, blank=True)
    final_ec = models.FloatField(null=True, blank=True)
    final_ph = models.FloatField(null=True, blank=True)
    do = models.FloatField(null=True, blank=True)
    photos = ArrayField(models.URLField(), null=True, blank=True)
    nutrition_stage = models.CharField(max_length=50)
    temperature = models.FloatField()
    final_temperature = models.FloatField(null=True, blank=True)
    water_quantity = models.FloatField()
    new_water_quantity = models.FloatField(null=True, blank=True)
    remarks = ArrayField(models.CharField(max_length=50))
    remarks_quantity = models.IntegerField(default=0, null=True, blank=True)
    quantity = models.CharField(max_length=50, null=True, blank=True)
    additional_details = models.CharField(max_length=50, null=True, blank=True)
    ph_correction = models.CharField(max_length=50, null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)

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

    @property
    def temperature_in_c(self):
        return f"{self.temperature} °C"

    class Meta:
        verbose_name = "Inner Water Tank"
        verbose_name_plural = "Inner Water Tank"


class CoolingPad(BaseModel):
    """
    Model to store cooling pad data
    """

    ph = models.FloatField()
    ec = models.FloatField()
    tank_temperature = models.FloatField()
    remarks = ArrayField(models.CharField(max_length=100))

    @property
    def tank_temperature_in_c(self):
        return f"{self.tank_temperature} °C"

    class Meta:
        verbose_name = "Cooling Pad"
        verbose_name_plural = "Cooling Pad"
