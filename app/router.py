import os

from datetime import datetime

from fastapi import Body, status, APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models import GamePlayers, GameMove, RageQuit, User, ShowUser
from app.schemas import Base, User_db
from app.database import *
from app.logic import Logic
from app.hashing import Hashing

router = APIRouter()
logic = Logic()

@router.post(
    "/user",
    response_model=ShowUser,
    response_description="Create user.",
    tags=["user"]
    )
def create_user(request: User, db: Session = Depends(get_db)):
        new_user = User_db(name=request.name,email=request.email,password=Hashing.bcrypt(request.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


@router.get(
    "/user/{id}",
    response_model=ShowUser,
    response_description="Get user data without password.",
    tags=["user"]
)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User_db).filter(User_db.id == id).first()
    if not user:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=jsonable_encoder({"detail": f"User with id {id} is not available"})
        )
    return user


@router.post(
    "/game",
    response_description="Creates game.",
    response_model=GamePlayers,
    tags=["game"]
)
async def game_create(
    body: GamePlayers = Body(...),
    db: Session = Depends(get_db)
):
    obj = jsonable_encoder(body)

    logic.create(
        player1=obj['player1'],
        player2=obj['player2']
    )
    logic.create_state(db)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder({"detail": logic.status()}))



@router.put(
    "/game",
    response_description="Commits move.",
    response_model=GameMove,
    tags=["game"]
)
async def game_move(
    body: GameMove = Body(...),
    db: Session = Depends(get_db)
):
    obj = jsonable_encoder(body)

    y = logic.move(
        player_id=obj['player_id'],
        coordinate=obj['coordinate']
    )

    if y != 0:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=jsonable_encoder({"detail": logic.status(), "error": y}))
    else:
        logic.save_state(db)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder({"detail": logic.status()}))

@router.delete(
    "/game",
    response_description="Rage quit.",
    response_model=RageQuit,
    tags=["game"]
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
    tags=["game"]
)
async def game_status():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"detail": logic.status()}))



@router.get(
    "/health",
    response_description="Healthcheck",
)
async def healthcheck():
    Base.metadata.create_all(bind=engine)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="OK")

@router.get(
    "/json/test"
)
def json_test():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"detail": logic.toJSON()}))

@router.get(
    "/db/create"
)
def db_create():
    init_db()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder({"detail": "Database created"}))


# @router.get(
#     "/json/test"
# )
# def json_test():
