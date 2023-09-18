# django imports
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# project imports
from farms.models import Farm


class User(AbstractUser):
    class Role(models.IntegerChoices):
        ADMIN = 0, _("Admin")
        FARM_MANAGER = 1, _("Farm Manager")
        AREA_MANAGER = 2, _("Area Manager")
        OPERATIONS_MANAGER = 3, _("Operations Manager")
        FARM_EXECUTIVE = 4, _("Farm Executive")
        OTHER = 5, _("Other")

    role = models.IntegerField(
        choices=Role.choices,
        # default=1,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    farms = models.ManyToManyField(Farm, blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    def add_farm_in_group_to_user(self):
        for group in self.groups.all():
            farms = Farm.objects.filter(farm_group=group.name)
            self.farms.add(*farms)

    def __str__(self):
        return f"{self.username} | {self.first_name} {self.last_name}"
