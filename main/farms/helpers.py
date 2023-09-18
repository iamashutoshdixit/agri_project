# python imports
import boto3
from io import BytesIO
from PIL import Image

# django imports
from django.conf import settings

# project imports
from config.helpers import get_config


def get_issue_tracker_status():
    issue_tracker_statuses = get_config("issue_tracker_status")
    if not issue_tracker_statuses:
        return []
    return list(
        enumerate(
            map(lambda x: x.title(), issue_tracker_statuses["options"]),
            1,
        )
    )


def uploader(data, filename):

    file = BytesIO(data)
    picture = Image.open(file)
    AWS_ID = settings.AWS_ID
    AWS_KEY = settings.AWS_KEY
    BUCKET = settings.AWS_S3_BUCKET

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ID,
        aws_secret_access_key=AWS_KEY,
    )

    picture.save(f"/tmp/{filename}", "webp", optimize=True, quality=50)
    s3.upload_file(f"/tmp/{filename}", BUCKET, f"eeki-images/{filename}")
