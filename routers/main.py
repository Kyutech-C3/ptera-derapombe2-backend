from fastapi import APIRouter
from .users import user_router

base_router = APIRouter()
base_router.include_router(user_router, prefix='/users')
