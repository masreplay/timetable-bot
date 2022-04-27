import os
import uuid

import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import HTTPException, status, UploadFile

from app.core.config import settings

_s3 = boto3.client(
    's3',
    aws_access_key_id=settings().AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings().AWS_SECRET_ACCESS_KEY
)

_reusable_failed_upload_file = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Failed Uploading File"
)


def upload_to_aws_folder(local_file, folder_name, file_name):
    try:
        _s3.upload_fileobj(local_file, settings().AWS_BUCKET_NAME, f"{folder_name}/{file_name}")
        return True
    except NoCredentialsError:
        raise _reusable_failed_upload_file


def upload_image(image: UploadFile | None) -> str | None:
    if image:
        return upload_to_aws(image)


def upload_to_aws(image: UploadFile) -> str:
    try:
        file_name: str = str(uuid.uuid4()) + os.path.splitext(image.filename)[1]
        _s3.upload_fileobj(
            image.file,
            settings().AWS_BUCKET_NAME, file_name,
            ExtraArgs={"ACL": "public-read", "ContentType": "image"},
        )
        return f"{settings().S3_BASE_URL}/{file_name}"
    except NoCredentialsError:
        raise _reusable_failed_upload_file


def delete_from_s3(folder_name, file_name) -> bool:
    try:
        _s3.delete_object(Bucket=settings().AWS_BUCKET_NAME, Key=f'{folder_name}/{file_name}')
        return True
    except NoCredentialsError:
        raise _reusable_failed_upload_file


async def check_image_type(image):
    extensions = ["image/jpeg", "image/png", "image/jpg"]
    if image.content_type not in extensions:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"please upload a {','.join(extensions)} file",
        )
