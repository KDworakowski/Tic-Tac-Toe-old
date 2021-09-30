import pytest
import os
from sqlalchemy import create_engine, select
from sqlalchemy import Column, Date, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import jsonpickle

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
        # os.remove("user.db")

    request.addfinalizer(teardown)

    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    return SessionLocal()

class TestResource:
    # def create_state(self, resource):
    #     stmt = app.models.GameStatus(
    #         id=self.game.id,
    #         serialized_game_status=jsonpickle.encode(self.game)
    #     )
    #     resource.add(stmt)
    #     resource.commit()
    #     resource.refresh(stmt)

    def test_insert(self, resource):
        stmt = app.models.GameStatus(
            id=2,
            serialized_game_status=2324234334242343
        )
        resource.add(stmt)
        resource.commit()
        resource.refresh(stmt)

    def save_state(self, resource):
        stmt = resource.execute(select(app.models.GameStatus).filter_by(id=2)).scalar_one()
        stmt.serialized_game_status=00000
        # print(
        #     "SELF.ID:", self.game.id,
        #     "STMT:", stmt,
        #     "ID", id
        # )
        resource.add(stmt)
        resource.commit()
        resource.refresh(stmt)




    # def load_state(self, id, resource) -> bool:
    #     stmt = select([
    #         app.models.GameStatus.columns.id,
    #         app.models.GameStatus.columns.serialized_game_status]
    #     ).where(
    #         app.models.GameStatus.columns.id == id
    #     )
    #     self.game = jsonpickle.decode(result[0]["serialized_game_status"])
    #     return True
