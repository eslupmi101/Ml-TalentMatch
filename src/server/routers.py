from fastapi import APIRouter

from app.resume import resume_router

api_router = APIRouter()

api_router.include_router(resume_router)
