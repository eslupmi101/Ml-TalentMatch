import logging

from fastapi import HTTPException, UploadFile, status

from core.database import db, PyObjectId
from .ai import get_result
from .converter import convert_resume
from .upload import upload_resume

logger = logging.getLogger(__name__)


async def parse_resume(resume: UploadFile, api_key: str) -> dict:
    try:
        file_url = await upload_resume(resume)

        if not file_url:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Upload resume failed'
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Upload resume failed - {e}'
        )

    try:
        resume_string: str = await convert_resume(file_url)

        if not resume_string:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Convert resume failed'
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Convert resume failed - {e}'
        )

    try:
        result = await get_result(resume_string, api_key)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Get result from AI failed'
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Get result from ai failed - {e}'
        )

    # insert resume to database
    new_result = {**result}
    insertion_response = await db.resumes.insert_one(result)

    new_result["resume_id"] = str(insertion_response.inserted_id)
    new_result["source_link"] = file_url

    return new_result
