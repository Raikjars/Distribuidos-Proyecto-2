from fastapi import APIRouter
from api.routes import router as message_router

router = APIRouter()

router.include_router(message_router, prefix="/v1", tags=["Artists"])