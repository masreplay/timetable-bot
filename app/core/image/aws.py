import os
import uuid

import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import HTTPException, status, UploadFile

from app.core.config import settings

s3 = boto3.client(
    's3',
    aws_access_key_id=settings().AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings().AWS_SECRET_KEY
)

reusable_failed_upload_file = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Failed Uploading File"
)


def upload_to_aws_folder(local_file, folder_name, file_name):
    try:
        s3.upload_fileobj(local_file, settings().BUCKET_NAME, f"{folder_name}/{file_name}")
        return True
    except NoCredentialsError:
        raise reusable_failed_upload_file


def upload_to_aws(image: UploadFile) -> str:
    try:
        file_name: str = str(uuid.uuid4()) + os.path.splitext(image.filename)[1]

        s3.upload_fileobj(
            image.file,
            settings().BUCKET_NAME, file_name,
            ExtraArgs={"ACL": "public-read", "ContentType": "image"},
        )
        return f"https://{settings().B}.s3.eu-west-2.amazonaws.com//{file_name}"
    except NoCredentialsError:
        raise reusable_failed_upload_file


def delete_from_s3(folder_name, file_name) -> bool:
    try:
        s3.delete_object(Bucket=settings().BUCKET_NAME, Key=f'{folder_name}/{file_name}')
        return True
    except NoCredentialsError:
        raise reusable_failed_upload_file


async def check_image_type(image):
    extensions = ["image/jpeg", "image/png", "image/jpg"]
    if image.content_type not in extensions:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"please upload a {','.join(extensions)} file",
        )
