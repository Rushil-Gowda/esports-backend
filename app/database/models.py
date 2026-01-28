from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import EmailStr
from sqlalchemy import Column,Enum as SAEnum
from sqlmodel import Field, SQLModel


class User(SQLModel, table = True):
    
    id: int = Field(default=None, primary_key=True)
    name: str 
    email: EmailStr = Field(unique=True)
    password_hash: str


class ContactMode(str, Enum):
    whatsapp = "whatsapp"
    discord = "discord"
    instagram = "instagram"


class PaymentStatus(str, Enum):
    pending = "pending"
    verified = "verified"
    rejected = "rejected"

class Tournament(SQLModel,table = True):
    __tablename__ = "tournament"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True
    )

    name: str = Field(index=True)
    game: str 
    price: int

    entry_fee: int
    max_teams: int
    cur_teams: int

    start_date: datetime

    created_at: datetime = Field(default_factory=datetime.utcnow)



class ValorantRegistration(SQLModel, table = True):
    __tablename__ = "valorant_registration"

    id: int | None = Field(default=None, primary_key=True)
    team_name: str
    team_logo_url: Optional[str] = Field(default=None)
    # tournament_id: str = Field(foreign_key="tournament.id", index=True)
    captain_name: str
    captain_ign: str
    email: EmailStr
    phone: int = Field(unique=True)

    preferred_contact: ContactMode = Field(
        sa_column= Column(SAEnum(ContactMode))
    )

    payment_status: PaymentStatus = Field(
        default=PaymentStatus.pending,
        sa_column=Column(SAEnum(PaymentStatus))
    )

    payment_utr: Optional[str] = Field(default=None)
    payment_screenshot_url: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.utcnow)


class PlayerRole(str, Enum):
    captain = "CAPTAIN"
    player = "PLAYER"
    substitute = "SUBSTITUTE"


class Player(SQLModel, table=True):
    __tablename__ = "player"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True
    )

    team_registration_id: int = Field(
        foreign_key="valorant_registration.id",
        index=True
    )

    role: PlayerRole = Field(
        sa_column=Column(SAEnum(PlayerRole))
    )

    real_name: str
    ign: str
    riot_id_tag: str
