# python imports
import time

# django imports
from django.http import HttpResponse


def generate_id():
    pass


def generate_image_tag(url):
    return f"""<img src="{url}"></img>"""


def csv_dispatcher(content):
    """
    Convert content to csv and send as downlooad
    """
    filename = int(time.time())
    response = HttpResponse(content, content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}.csv"'
    return response
