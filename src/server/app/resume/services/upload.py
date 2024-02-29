import uuid

from fastapi import UploadFile

from core.media_storage import client as minio_client
from core.media_storage import minio_endpoint
from core.settings import settings


async def upload_resume(
    resume: UploadFile
) -> str:
    # Change filename to almost unique filename with a video format
    resume.filename = str(uuid.uuid4()) + '.' + resume.filename.split('.')[-1]

    # Directory for resumes
    directory = 'resumes'
    minio_client.upload_file(
        file=resume,
        directory=directory
    )

    scheme = 'https://' if settings.MINIO_SECURE else 'http://'
    url = f'{scheme}{minio_endpoint}/{settings.MINIO_BUCKET_NAME}/{directory}/{resume.filename}'

    return url
