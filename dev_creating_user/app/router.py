from fastapi import Body, status, APIRouter, Depends

from app.models import Base, Users, User

from .database import SessionLocal, engine

from sqlalchemy.orm import Session

from .hashing import Hashing


router = APIRouter()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@router.post("/user")
def create_user(request: User, db: Session = Depends(get_db)):
    new_user = Users(name=request.name,password=Hashing)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
