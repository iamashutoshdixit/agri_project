# django imports
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import (
    user_logged_in,
    user_login_failed,
    user_logged_out,
)
import logging

# project imports
from users.models import User
from labour.models import Labour

logger = logging.getLogger("auth")


@receiver(post_save, sender=User)
def create_lab_for_farm_man_exec(sender, instance, created, **kwargs):
    if instance.role in (1, 4):
        try:
            obj, created = Labour.objects.get_or_create(
                name=f"{instance.first_name} {instance.last_name}",
                is_staff=True,
                user_id=instance.id,
            )
        except Labour.MultipleObjectsReturned:
            return
        if created:
            obj.farms.set(instance.farms.all())


# logging user auth logs
@receiver(user_logged_in)
def post_login(user, **kwargs):
    logger.info(f"User: {user.username} logged in")


@receiver(user_logged_out)
def post_logout(sender, request, user, **kwargs):
    logger.info(f"User: {user.username} logged out")


@receiver(user_login_failed)
def post_login_fail(sender, credentials, request, **kwargs):
    logger.info(f"Login failed with credentials: {credentials}")
