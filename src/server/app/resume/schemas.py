from fastapi import HTTPException, UploadFile
from pydantic import BaseModel, validator

from .constants import VALID_TYPE_RESUME_FILE
from .utils import form_body


@form_body
class ResumeUpload(BaseModel):
    file: UploadFile
    api_key: str

    @validator('file')
    def check_file_type(cls, file: UploadFile):
        """Check if file type is allowed."""
        file_extension = file.filename.split('.')[-1]
        if file_extension not in VALID_TYPE_RESUME_FILE:
            raise HTTPException(
                status_code=400, detail=f'Uploaded file has invalid type - {file_extension} '
            )

        return file


class ResumeResponse(BaseModel):
    resume: dict
