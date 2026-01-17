
from datetime import datetime, timedelta
from fastapi import HTTPException,status
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from sqlmodel import select
from app.api.schemas.user import UserCreate
from app.database.models import User
from app.config import security_settings
from app.utils import generate_access_token

password_context = CryptContext(schemes=["argon2"], deprecated="auto")

class UserService:
    def __init__(self,session : AsyncSession):
        self.session = session

    async def add(self,credentials:UserCreate) -> User:
        user = User(
            **credentials.model_dump(exclude=["password"]),
            password_hash = password_context.hash(credentials.password)
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user
    
    async def token(self,email,password) -> str:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )

        user = result.scalar()

        if user is None or not password_context.verify(password,user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="email or password is incorrect",
            )

        token = generate_access_token(data={
            "user":{
                "name":user.name,
                "id":user.id,
            }
        })

        return token
    
