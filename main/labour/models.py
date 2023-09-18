# python imports

# django imports
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe
from django.db import models

# user imports
from libs.helpers import generate_image_tag
from farms.models import Farm
from libs.models import BaseTemplateWithActor


class Labour(BaseTemplateWithActor):
    name = models.CharField(max_length=50)
    mobile = models.BigIntegerField(
        validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(1000000000),
        ],
        null=True,
        blank=True,
    )
    photo = models.URLField(null=True, blank=True)
    kyc_type = models.IntegerField(
        choices=[
            (0, "Aadhar Card"),
            (1, "PAN Card"),
            (2, "Voter Card"),
            (3, "Family Card"),
        ],
        null=True,
        blank=True,
    )
    kyc_number = models.BigIntegerField(null=True, blank=True)
    kyc_front = models.URLField(null=True, blank=True)
    kyc_back = models.URLField(null=True, blank=True)
    is_staff = models.BooleanField(default=False, editable=False)
    user_id = models.IntegerField(null=True, blank=True, editable=False)
    farms = models.ManyToManyField(Farm)

    def clean(self):
        errors = {}
        required_fields = [
            "mobile",
            "photo",
            "kyc_type",
            "kyc_number",
            "kyc_front",
            "kyc_back",
        ]
        if not self.is_staff:
            for field in required_fields:
                if getattr(self, field) is None:
                    errors[field] = "This field is required."
        if errors:
            raise ValidationError(errors)

    @property
    def kyc_images(self):
        return mark_safe(
            f"""
        <div>
            {generate_image_tag(self.kyc_front)}
            {generate_image_tag(self.kyc_back)}
        </div>
        """
        )

    def __str__(self):
        return f"{self.name}"


class Attendance(BaseTemplateWithActor):
    """
    Model to store attendance details for labours
    """

    labour = models.ForeignKey(Labour, on_delete=models.PROTECT)
    farm = models.ForeignKey(
        Farm,
        on_delete=models.PROTECT,
        related_name="labour_farm",
    )
    action = models.IntegerField(
        choices=[
            (0, "PUNCH IN"),
            (1, "PUNCH OUT"),
            (2, "ABSENT"),
        ]
    )
    datetime = models.DateTimeField(null=True)

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendance"


class Work(BaseTemplateWithActor):
    """
    Model to store work related data for labour
    """

    farm = models.ForeignKey(
        Farm,
        on_delete=models.PROTECT,
    )
    labour = models.ForeignKey(Labour, on_delete=models.PROTECT)
    duration = models.IntegerField(default=0)
    description = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    work_quantity = models.IntegerField(default=0)
    recipe = models.JSONField(null=True)
    recipe_quantity = models.IntegerField(null=True, blank=True)
    water_quantity = models.IntegerField(null=True, blank=True)
    dome = models.IntegerField(default=0)
    remarks = ArrayField(models.CharField(max_length=50))

    class Meta:
        verbose_name = "Labour Work"
        verbose_name_plural = "Labour Work"
