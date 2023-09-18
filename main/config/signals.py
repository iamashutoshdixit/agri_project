# python imports
from datetime import datetime

# django imports
from django.db.models.signals import post_save
from django.dispatch import receiver

# app imports
from .models import Config


@receiver(post_save, sender=Config)
def config_post_save_handler(sender, created, instance, **kwargs):
    if instance.key == "last_updated":
        return

    # update or create last_update config
    Config.objects.update_or_create(
        key="last_updated",
        defaults={
            "value": {
                "date": str(datetime.now().date()),
                "time": str(datetime.now().time()),
            }
        },
    )
