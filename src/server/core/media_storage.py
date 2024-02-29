import json
from urllib.parse import urlparse

from fastapi import HTTPException, UploadFile, status
from minio import Minio

from .utils import file_size
from core.settings import settings


class MinioClient:
    def __init__(
        self, endpoint: str, access_key: str, secret_key: str, bucket_name: str
    ):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=settings.MINIO_SECURE,
        )
        self.bucket_name = bucket_name

    def create_bucket(self):
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def set_bucket_policy(self):
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{self.bucket_name}/*"
                }
            ]
        }

        try:
            self.client.set_bucket_policy(self.bucket_name, json.dumps(policy))
        except Exception as e:
            self._exception(f'Error while trying to set bucket policy. Exception: {e}')

    def upload_file(self, file: UploadFile, directory: str):
        try:
            object_name = f'{directory}/{file.filename}'
            return self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=file.file,
                length=file_size(file)
            )
        except Exception as e:
            self._exception(f'Error while trying to upload file. Exception: {e}')

    def download_file(self, source: str, destination: str):
        try:
            self.client.fget_object(self.bucket_name, source, destination)
        except Exception as e:
            self._exception(f'Error while trying to download file. Exception: {e}')

    def delete_file(self, destination: str):
        """
        Delete object in minio by url of object.
        """
        try:
            parsed_url = urlparse(destination)
            # remove blunk string and bucket name
            path = parsed_url.path.split('/')[2:]
            object_name = '/'.join(path)
            self.client.remove_object(self.bucket_name, object_name)
        except Exception as e:
            self._exception(f'Error while trying to remove file. Exception: {e}')

    def _exception(self, detail: str):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


minio_endpoint = f'{settings.MINIO_HOST}:{settings.MINIO_PORT}'


client = MinioClient(
    endpoint=minio_endpoint,
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    bucket_name=settings.MINIO_BUCKET_NAME
)
