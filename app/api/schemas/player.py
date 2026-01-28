from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class PlayerRole(str, Enum):
    CAPTAIN = "CAPTAIN"
    PLAYER = "PLAYER"
    SUBSTITUTE = "SUBSTITUTE"

class ContactMode(str, Enum):
    whatsapp = "whatsapp"
    discord = "discord"
    instagram = "instagram"

class PlayerCreate(BaseModel):
    role: PlayerRole
    real_name: str
    ign: str
    riot_id_tag: str

class PlayerRead(PlayerCreate):
    id: int

class LeaderCreate(BaseModel):
    name: str
    ign: str
    email: str
    phone: str
    preferred_contact: ContactMode

class PaymentCreate(BaseModel):
    utr: str
    screenshot_url: str

class TeamRegistrationCreate(BaseModel):
    team_name: str
    team_logo_url: Optional[str] = None

    captain_name: str
    captain_ign: str
    email: EmailStr
    phone: int
    preferred_contact: ContactMode

    payment_utr: Optional[str] = None
    payment_screenshot_url: Optional[str] = None

    players: List[PlayerCreate]

class TeamRegistrationRead(BaseModel):
    id: int
    tournament_id: int
    user_id: int

    team_name: str
    team_logo_url: Optional[str]

    captain_name: str
    captain_ign: str
    email: str
    phone: str
    preferred_contact: ContactMode

    payment_status: str
    payment_utr: Optional[str]
    payment_screenshot_url: Optional[str]

    created_at: datetime

    players: List[PlayerRead]
