import pytest
import os
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.database import Base

import app.models
from app.logic import Logic

@pytest.fixture()
def resource(request):

    print("setup")

    SQLALCHEMY_DATABASE_URL = 'sqlite:///./school.db'

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        echo=True
    )

    Base.metadata.create_all(engine)

    def teardown():
        print("teardown")

        os.remove("school.db")

    # request.addfinalizer(teardown)

    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    return SessionLocal()

class TestResource:
    def test_insert(self, resource):
        stmt = app.models.GameStatus(
            id=2,
        )
        stmt.serialized_game_status=1
        resource.add(stmt)
        resource.commit()
        resource.refresh(stmt)

# def test_answer():
#     password_length = 8
#     p = PasswordGenerator(length=int(password_length))
#     password = p.password_generator()

#     assert password_length == len(password)
