# app imports
from .models import Config


def get_config(key):
    config = Config.objects.filter(key=key).first()
    value = {}
    if config:
        value = config.value
    return value
