from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

### GameStatus


def get_game_status(db: Session, game_id: int):
    return db.query(models.GameStatus).filter(models.GameStatus == game_id).first()

def get_games_statuses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GameStatus).offset(skip).limit(limit).all()

def create_game_status(db: Session, game_status: schemas.GameStatusCreate):
    serialized_game_status = game_status.serialized_game_status + "serialized_game_status" ## Serialized game status
    db_game_status  = models.GameStatus(serialized_game_status=game_status.serialized_game_status)
    db.add(db_game_status)
    db.commit()
    db.refresh(db_game_status)
    return db_game_status
