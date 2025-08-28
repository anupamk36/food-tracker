import os
import boto3
from app.core.config import settings
from typing import Tuple

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

def save_file_local(file_obj, filename: str) -> str:
    path = os.path.join(settings.UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(file_obj.read())
    return path

def upload_to_s3(local_path: str, key: str) -> str:
    # returns s3 key or url
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION,
    )
    s3.upload_file(local_path, settings.S3_BUCKET, key)
    return f"s3://{settings.S3_BUCKET}/{key}"
