import os
from datetime import datetime

from fastapi import Body, status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.models import GamePlayers, GameMove, RageQuit
from app.logic import Logic

router = APIRouter()
logic = Logic()

@router.post(
    "/game",
    response_description="Creates game.",
    response_model=GamePlayers
)
async def game_create(
    body: GamePlayers = Body(...)
):
    obj = jsonable_encoder(body)
    logic.create(
        player1=obj['player1'],
        player2=obj['player2']
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder({"detail": logic.status()}))


@router.put(
    "/game",
    response_description="Commits move.",
    response_model=GameMove
)
async def game_move(
    body: GameMove = Body(...)
):
    obj = jsonable_encoder(body)

    if not logic.move(
        player_id=obj['player_id'],
        coordinate=obj['coordinate']
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=jsonable_encoder({"detail": logic.status()}))
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder({"detail": logic.status()}))


@router.delete(
    "/game",
    response_description="Rage quit.",
    response_model=RageQuit
)
async def game_rage_quit(
    body: RageQuit = Body(...)
):
    obj = jsonable_encoder(body)

    if not logic.ragequit(player_id=obj['player_id']):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=jsonable_encoder({"detail": logic.status()}))
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder({"detail": logic.status()}))


@router.get(
    "/game",
    response_description="Getting game status.",
)
async def game_status():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"detail": logic.status()}))


@router.get("/health", response_description="Healthcheck")
async def healthcheck():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="OK")
