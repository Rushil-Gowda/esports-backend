from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import UserServiceDep, SessionDep
from app.api.schemas.user import UserCreate, UserRead
from app.database.models import User
from app.core.security import oauth2_scheme
from app.utils import decode_access_token

router = APIRouter(prefix="/user", tags=["User"])  # ✅ lowercase


@router.post("/signup", response_model=UserRead)
async def register_user(user: UserCreate, service: UserServiceDep):
    return await service.add(user)


@router.post("/token")
async def login_user(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserServiceDep,
):
    token = await service.token(
        request_form.username,
        request_form.password,
    )

    return {
        "access_token": token,
        "token_type": "bearer",  
    }


@router.get("/dashboard")
async def get_dashboard(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
):
    data = decode_access_token(token)

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
        )

    user = await session.get(User, data["user"]["id"])
    return user
