import os

from datetime import datetime

from fastapi import Body, status, APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import jsonpickle

import app.models
import app.schemas

from app.database import SessionLocal, engine, Base
from app.logic import Logic
from app.hashing import Hashing

router = APIRouter()
logic = Logic()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/user",
    response_model=app.schemas.ShowUser,
    response_description="Create user.",
    tags=["user"]
    )
def create_user(request: app.schemas.User, db: Session = Depends(get_db)):
        new_user = User_db(name=request.name,email=request.email,password=Hashing.bcrypt(request.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


@router.get(
    "/user/{id}",
    response_model=app.schemas.ShowUser,
    response_description="Get user data without password.",
    tags=["user"]
)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(app.schemas.User).filter(User_db.id == id).first()
    if not user:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=jsonable_encoder({"detail": f"User with id {id} is not available"})
        )
    return user


@router.post(
    "/game",
    response_description="Creates game.",
    response_model=app.schemas.GamePlayers,
    tags=["game"]
)
async def game_create(
    body: app.schemas.GamePlayers = Body(...),
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
    response_model=app.schemas.GameMove,
    tags=["game"]
)
async def game_move(
    body: app.schemas.GameMove = Body(...),
    db: Session = Depends(get_db)
):
    obj = jsonable_encoder(body)
# {'id': 'b32a8e9a-edc5-52b2-937f-30bba0e7e911', 'player1': 'dupa', 'player2': 'dupsko', 'player_turn': 1, 'board': \
# [[0, 0, 0], [0, 0, 0], [0, 0, 0]], 'score_board': {'dupa': 0, 'dupsko': 0}, 'player_win': 0}

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
    response_model=app.schemas.RageQuit,
    tags=["game"]
)
async def game_rage_quit(
    body: app.schemas.RageQuit = Body(...)
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
def db_create(db: Session = Depends(get_db)):
    # app = FastAPI()
    # db = sqlalchemy(app)

    # db.create_all()
    # db.session.commit()

    # admin = User('admin', 'admin@example.com', 'dupa123')
    # db.session.add(admin)
    # db.session.commit()

    db.create_all()
    db.session.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder({"detail": "Database created"}))


# @router.get(
#     "/json/test"
# )
# def json_test():
