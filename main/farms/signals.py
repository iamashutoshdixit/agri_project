# python imports
import requests
import logging

# django imports
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import Group
from notifications.signals import notify
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

# app imports
from .models import Camera, IOTBox, IssueTracker, Farm
from .models import IssueTracker

logger = logging.getLogger(__name__)

BASE_URL = settings.CSS_URL


def get_streams():
    # get streams list
    url = f"{BASE_URL}/streams"
    return requests.get(url).json()["payload"]


def get_stream_info(stream_id):
    # get information abouth the stream
    url = f"{BASE_URL}/stream/{stream_id}/info"
    return requests.get(url).json()["payload"]


def add_stream(stream_id, name=""):
    # add a stream
    data = {
        "name": name,
    }
    url = f"{BASE_URL}/stream/{stream_id}/add"
    res = requests.post(url, json=data).json()["status"]
    if res == 1:
        return data
    return {}


def update_stream(stream_id, stream_data):
    # update a stream metadata
    url = f"{BASE_URL}/stream/{stream_id}/edit"
    res = requests.post(url, json=stream_data).json()["status"]
    if res == 1:
        return stream_data
    return {}


@receiver(post_save, sender=Camera)
def add_stream_to_rtsp(sender, instance, created, **kwargs):
    # Add stream when a camrea model is added
    available_streams = get_streams()

    stream_id = instance.farm.name.lower()
    stream_name = f"Farm {instance.farm.name} Camera Streams"
    channel = instance.channel
    camera_url = instance.url
    if stream_id not in available_streams:
        stream_data = add_stream(stream_id, name=stream_name)

    else:
        stream_data = available_streams[stream_id]
    channels = stream_data.get("channels", {})
    channels[channel] = {
        "url": camera_url,
        "on_demand": True,
    }
    stream_data["channels"] = channels
    update_stream(stream_id, stream_data)


@receiver(post_save, sender=IssueTracker)
def send_notification(sender, instance, created, **kwargs):
    # sends notification to assignee
    if created:
        notify.send(instance, recipient=instance.assignee, verb="was created")
        device = FCMDevice.objects.filter(user=instance.assignee).last()
        message_title = "Issue Tracker"
        message_body = f"{instance.issue} has been assigned to you"
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
    # sends notification to user raised the issue
    else:
        notify.send(instance, recipient=instance.assignee, verb="was updated")
        device = FCMDevice.objects.filter(user=instance.created_by).last()
        message_title = "Issue Tracker"
        message_body = f"{instance.issue} status has been updated"
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


@receiver(post_save, sender=Farm)
def assign_farm_to_users_in_same_group(sender, instance, created, **kwargs):
    group = Group.objects.filter(name=instance.farm_group).first()
    if group is None:
        return
    for user in group.user_set.all():
        user.farms.add(instance)


@receiver(post_save, sender=IOTBox)
def map_farm_to_iotbox(sender, instance, created, **kwargs):
    if instance.is_active is False and instance.farm is not None:
        instance.farm.iotbox = None
        instance.farm.save()
        instance.farm = None
        instance.save()


@receiver(post_save, sender=Farm)
def assign_iotbox_to_farm(sender, instance, created, **kwargs):
    if instance.iotbox is not None:
        instance.iotbox.farm = instance
        instance.iotbox.save()
