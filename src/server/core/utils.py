from os import fstat, path, remove

from fastapi import UploadFile

from core.database import PyObjectId
from core.settings import settings


def remove_file(filename: str, user_id: PyObjectId) -> None:
    file_path = f"{settings.TEMP_FOLDER}/{user_id}/{filename}"
    if path.exists(file_path):
        remove(file_path)


def file_size(file: UploadFile) -> int:
    return fstat(file.file.fileno()).st_size
