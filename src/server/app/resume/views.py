from fastapi import APIRouter, Depends, Path, status

from core.schemas import ExceptionModel

from .schemas import ResumeResponse, ResumeUpload
from .services.data_parser import parse_resume

resume_router = APIRouter(prefix='/resumes', tags=['resume'])


@resume_router.post(
    '/',
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ExceptionModel},
    },
    tags=['resume'],
    dependencies=[]
)
async def resume_upload(
    data: ResumeUpload = Depends(),
):
    if result := await parse_resume(data.file, data.api_key):
        return result
