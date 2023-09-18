from django.apps import AppConfig


class FarmManagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "farms"

    def ready(self):
        from . import signals
