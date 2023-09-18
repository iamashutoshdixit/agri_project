# python imports
import json

# django imports
from django.db import models


class Config(models.Model):
    """
    model to store config values as key, pair and tag values
    """

    key = models.CharField(
        max_length=20,
        default="",
        primary_key=True,
        unique=True,
    )
    value = models.JSONField(
        default=dict,
        null=True,
        blank=True,
    )
    tag = models.CharField(
        max_length=20,
        default="",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        value = json.dumps(self.value).lower()
        key = self.key.lower()
        self.key = key
        self.value = json.loads(value)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.key}"
