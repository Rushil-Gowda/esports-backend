from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy import select

from app.api.dependencies import SessionDep
from app.api.schemas.player import TeamRegistrationCreate
from app.core.security import oauth2_scheme
from app.database.models import Player, Tournament, ValorantRegistration
from app.utils import decode_access_token

router = APIRouter(prefix="/tournaments",tags=["Tournaments"])

@router.post("/{tournament_id}/register",status_code=201)
async def resgister_team(
    payload: TeamRegistrationCreate,
    session: SessionDep,
):
    # tournament = await session.get(Tournament, tournament_id)
    # if not tournament:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="Tournament not found",
    #     )

    # if tournament.cur_teams >= tournament.max_teams:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Tournament is full",
    #     )
    
    existing = await session.exec(
        select(ValorantRegistration).where(
            # ValorantRegistration.tournament_id == tournament_id,
            ValorantRegistration.email == payload.email,
        )
    )

    if existing.first():
            raise HTTPException(
            status_code=409,
            detail="This email is already registered for the tournament",
        )
    
    existing = await session.exec(
        select(ValorantRegistration).where(
            # ValorantRegistration.tournament_id == tournament_id,
            ValorantRegistration.phone == payload.phone,
        )
    )

    if existing.first():
            raise HTTPException(
            status_code=409,
            detail="This phone is already registered for the tournament",
        )


    team = ValorantRegistration(
        # tournament_id=tournament_id,

        team_name=payload.team_name,
        team_logo_url=payload.team_logo_url,

        captain_name=payload.captain_name,
        captain_ign=payload.captain_ign,
        email=payload.email,
        phone=payload.phone,
        preferred_contact=payload.preferred_contact,

        payment_utr=payload.payment_utr,
        payment_screenshot_url=payload.payment_screenshot_url,
    )

    session.add(team)
    await session.commit()
    await session.refresh(team)

    players_to_add = []

    for player in payload.players:
        players_to_add.append(
              Player(
                   team_registration_id=team.id,
                   role=player.role,
                   real_name=player.real_name,
                   ign=player.ign,
                   riot_id_tag=player.riot_id_tag,
              )
        )
    

    session.add_all(players_to_add)
    # tournament.cur_teams += 1
    # session.add(tournament)

    await session.commit()

    return {
         "message":"Team registered successfully",
         "registration_id": team.id,
    }