import os
from datetime import datetime

from fastapi import Body, status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.models import GamePlayers
from app.logic import Logic

router = APIRouter()
logic = Logic()

#     response_description="Create user entry.",
#     response_model=bday.InputModel)
# async def put_user(user_id: str, body: bday.InputModel = Body(...)):

@router.post(
    "/game",
    response_description="Creates game.",
    response_model=GamePlayers
)
async def game_create(
    body: GamePlayers = Body(...)
):
    input_obj = jsonable_encoder(body)
    logic.create(input_obj['player1'], input_obj['player2'])
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content="OK")


@router.put("/game")
async def game_move():
    place_on_table_not_occupied = True
    player_turn = True
    game_over = False

    if \
        not place_on_table_not_occupied or \
        not player_turn:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content="NOK")
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="OK")


@router.delete("/game")
async def game_rage_quit():
    game_over = False

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="OK")


@router.get("/game")
async def game_status():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"detail": logic.status()}))



# @router.get(
#     "/hello/{user_id}",
#     response_description="Create user entry.")
# async def get_user(user_id: str):
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content=jsonable_encoder({"detail": user_id})
#     )

@router.get("/health", response_description="Healthcheck")
async def healthcheck():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="OK")
