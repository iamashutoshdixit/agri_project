# python imports
import logging

# django imports
from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

# project imports
from users.models import User

# app imports
from .models import Reimbursement

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Reimbursement)
def send_notification(sender, instance, created, **kwargs):
    # sends notifications to particular group if created
    if created:
        users = User.objects.filter(groups__name="Reimbursement | Create")
        if users.count() == 0:  # Don't send notifications if no user's in group.
            return
        for user in users:
            device = FCMDevice.objects.filter(user=user).last()
            message_title = "Reimbursement"
            message_body = (
                f"New Reimbursement has been created by {instance.created_by}"
            )
            try:
                device.send_message(
                    Message(
                        notification=Notification(
                            title=message_title,
                            body=message_body,
                        )
                    )
                )
            except Exception:
                logger.error("Error sending push notifications", exc_info=True)
    # sends notification to user created the Reimbursement
    else:
        device = FCMDevice.objects.filter(user=instance.created_by).last()
        message_title = "Reimbursement"
        message_body = f"Status of your Reimbursement with invoice no {instance.invoice_no} has been updated"
        try:
            device.send_message(
                Message(
                    notification=Notification(
                        title=message_title,
                        body=message_body,
                    )
                )
            )
        except Exception:
            logger.error("Error sending push notifications", exc_info=True)
