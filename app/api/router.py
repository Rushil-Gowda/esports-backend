from fastapi import APIRouter
from .routers import  user,player


master_router = APIRouter()

master_router.include_router(player.router)
master_router.include_router(user.router)