from fastapi import APIRouter

from app.resume.views import resume_router

api_router = APIRouter(prefix='/api/v1')

api_router.include_router(resume_router)
