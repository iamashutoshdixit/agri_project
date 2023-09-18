# project imports
from libs.mixins import BaseMixin
from pdc.admin import my_admin

# app imports
from .models import Config


class ConfigAdmin(BaseMixin):
    list_display = [
        "key",
        "value",
        "tag",
    ]


my_admin.register(Config, ConfigAdmin)
