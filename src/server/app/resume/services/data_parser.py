import logging

from fastapi import HTTPException, UploadFile, status
from langchain_openai import ChatOpenAI

from core.database import db
from .evaluator import evaluate_response
from .ai import get_result
from .upload import upload_resume
from .converter import convert_resume

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
        resume_string = await convert_resume(file_url)

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
    jpeg_url = None

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

    chat = ChatOpenAI(
        temperature=0.0, api_key=api_key,
        model_name="gpt-4-turbo-preview"
    )
    new_result = {
        "resume": {**result},
        "score": await evaluate_response(chat, result, resume_string)
    }

    new_result["resume"]["source_link"] = file_url

    insertion_response = await db.resumes.insert_one(new_result)
    new_result["resume"]["resume_id"] = str(insertion_response.inserted_id)

    return new_result

