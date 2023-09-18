# python imports
import uuid
import re

# django imports
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator as Max,
    MinValueValidator as Min,
)
from django.db import models
from django.utils.html import mark_safe

# project imports
from libs.helpers import generate_image_tag
from libs.models import BaseTemplate, BaseTemplateWithActor


def farm_name_validator(value):
    # validate farm name
    pattern = r"^[A-Z]{1,12}-[A-Z]$"
    if re.match(pattern, value):
        return value
    raise ValidationError(
        "Following format required for farm name: X-Y, where X is any\
        set of capital letters upto a length of\
        12, and Y is a single capital letter"
    )


class Farm(BaseTemplateWithActor):
    """
    model to store farm related data
    """

    class FarmType(models.IntegerChoices):
        NURSERY = 0, _("Nursery")
        COMMERCIAL = 1, _("Commercial")

    farm_code = models.CharField(max_length=15, editable=False)
    name = models.CharField(
        max_length=14, validators=[farm_name_validator], unique=True
    )
    mac_address = models.CharField(max_length=30, null=True)
    type = models.IntegerField(choices=FarmType.choices)
    no_of_domes = models.IntegerField(
        validators=[
            Max(100),
            Min(1),
        ],
    )
    no_of_trays = models.IntegerField(null=True, blank=True)
    no_of_growing_lines = models.IntegerField(
        validators=[
            Max(500),
            Min(1),
        ],
        null=True,
        blank=True,
    )
    no_of_irrigation_tanks = models.IntegerField(
        validators=[Max(50), Min(1)],
    )
    no_of_cooling_tanks = models.IntegerField(
        validators=[Max(50), Min(1)],
    )
    no_of_ro_tanks = models.IntegerField(
        validators=[Max(50), Min(1)],
    )
    no_of_rw_tanks = models.IntegerField(
        validators=[Max(50), Min(1)],
    )
    inverter_power_output = models.DecimalField(max_digits=6, decimal_places=3)
    farm_group = models.CharField(max_length=30)
    inverter_phasing = models.IntegerField(validators=[Max(3), Min(1)])
    battery_capacity = models.IntegerField(
        validators=[Max(1000), Min(1)],
        null=True,
        blank=True,
    )
    solar_power_output = models.DecimalField(max_digits=6, decimal_places=3)
    locality = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    iotbox = models.ForeignKey(
        "farms.IOTBox",
        on_delete=models.PROTECT,
        related_name="iotbox",
        null=True,
        blank=True,
    )

    # Optional fields
    area = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        null=True,
        blank=True,
    )
    length = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        null=True,
        blank=True,
    )
    width = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        null=True,
        blank=True,
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    direction = models.FloatField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)

    # Config fields
    rw_tank_config = models.JSONField(
        null=True,
        blank=True,
    )
    ro_tank_config = models.JSONField(
        null=True,
        blank=True,
    )
    irrigation_tanks_config = models.JSONField(
        null=True,
        blank=True,
    )
    cooling_tanks_config = models.JSONField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.farm_code

    def cameras(self):
        return mark_safe(
            f"""
            <a target="_blank" href="/farms/cameras/{self.id}">
                Show all
            </a>
        """
        )

    def clean(self):
        if self.type == 0 and self.no_of_trays is None:
            raise ValidationError(
                {"no_of_trays": "This field is required for nursery farms."}
            )
        if self.type == 1 and self.no_of_growing_lines is None:
            message = "This field is required for nursery farms."
            raise ValidationError(
                {
                    "no_of_growing_lines": message,
                }
            )

    def save(self, *args, **kwargs):
        if self.pk is None:
            uid = uuid.uuid4().hex[:4]
            name = self.name.split("-")[0][: min(4, len(self.name))]
            fid = f'{self.type}{self.name.split("-")[-1]}'
            self.farm_code = f"{name}-{fid}-{uid}".upper()
        super(Farm, self).save(*args, **kwargs)


class VisitorEntry(BaseTemplateWithActor):
    """
    model to store visitor entriies
    """

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    mobile_number = models.BigIntegerField(
        validators=[
            Min(1000000000),
            Max(9999999999),
        ]
    )
    purpose_of_visit = models.CharField(max_length=50)
    feedback = models.CharField(max_length=100)
    datetime = models.DateTimeField()

    class Meta:
        verbose_name = "Visitor Entry"
        verbose_name_plural = "Visitor Entries"


class IssueTracker(BaseTemplateWithActor):
    """
    model to store raised issues
    """

    component = models.CharField(max_length=200)
    issue = models.CharField(max_length=200)
    photos = ArrayField(models.URLField(), null=True, blank=True)
    farm = models.ForeignKey(
        Farm,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    actions = models.CharField(max_length=100)
    assignee = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, related_name="issuetracker_assignee"
    )
    priority = models.IntegerField(
        choices=[
            (1, "Low"),
            (2, "Medium"),
            (3, "High"),
            (4, "Urgent"),
            (5, "Critical"),
        ]
    )
    status = models.IntegerField()
    datetime = models.DateTimeField()

    def __str__(self):
        return f"Issue in {self.farm} | {self.component} - {self.issue}"

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
        verbose_name = "Issue Tracker"
        verbose_name_plural = "Issue Tracker"


class Camera(BaseTemplate):
    farm = models.ForeignKey(Farm, on_delete=models.PROTECT)
    name = models.CharField(max_length=20)
    channel = models.CharField(max_length=10, default="0")
    url = models.CharField(
        max_length=200,
        default="http://example.com",
    )

    @property
    def video(self):
        link = f"""
<link href="https://vjs.zencdn.net/7.18.1/video-js.css" rel="stylesheet" />
<video id="my-video" controls class="video-js" data-setup="{{}}">
<source
src="http://3.110.2.32:8083/stream/{self.farm.name.lower()}/channel/{self.channel}/hls/live/index.m3u8?token=abcd"
type="application/x-mpegURL">
</video>
<script src="https://vjs.zencdn.net/7.18.1/video.min.js"></script>
        """
        return mark_safe(link)

    def __str__(self):
        return f"{self.farm}:{self.name}:{self.channel}"


class IOTBox(BaseTemplateWithActor):
    farm = models.ForeignKey(
        Farm,
        on_delete=models.PROTECT,
        related_name="iotboxes",
        null=True,
        blank=True,
        editable=False,
    )
    serial_number = models.CharField(max_length=20, unique=True)
    uuid = models.CharField(max_length=50, default=uuid.uuid4, editable=False)
    params = models.JSONField(default=dict, null=True, blank=True)
    local_ip = models.CharField(max_length=16)
    mqtt_port = models.IntegerField()
    http_port = models.IntegerField()
    ssh_port = models.IntegerField()

    @property
    def farm_name(self):
        if not self.farm:
            return "N/A"
        return self.farm.name

    def __str__(self):
        return f"{self.id} | {self.serial_number} "

    class Meta:
        verbose_name = "IOT Box"
        verbose_name_plural = "IOT Boxes"


class FarmManagerAttendance(BaseTemplate):
    """
    Model to store attendance details for users (farm managers, etc)
    """

    farm = models.ForeignKey(Farm, on_delete=models.PROTECT)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="user",
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    action = models.IntegerField(
        choices=[
            (0, "PUNCH IN"),
            (1, "PUNCH OUT"),
        ]
    )

    class Meta:
        verbose_name = "Farm Manager Attendance"
        verbose_name_plural = "Farm Manager Attendance"
