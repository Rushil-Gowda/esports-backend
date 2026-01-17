from typing import Annotated

from fastapi import Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import oauth2_scheme
from app.database.models import User

from app.database.session import get_session
from app.services.user import UserService
from app.utils import decode_access_token


SessionDep = Annotated[AsyncSession,Depends(get_session)]

def get_user_service(session: SessionDep):
    return UserService(session)

UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service),
]
 
async def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]):

    data = decode_access_token(token)
    return data

async def get_current_user(token_data: Annotated[dict,Depends(get_access_token)],session:SessionDep):

    return await session.get(User,token_data["user"]["id"])



#seller dependency
UserDep = Annotated[User,Depends(get_current_user)]






