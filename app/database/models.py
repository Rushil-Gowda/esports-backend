from datetime import datetime
from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table = True):
    
    id: int = Field(default=None, primary_key=True)
    name: str 
    email: EmailStr = Field(unique=True)
    password_hash: str