import os

import databases
import sqlalchemy
from dotenv import load_dotenv
from fastapi_users import models
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

load_dotenv(dotenv_path="../.dev.env", verbose=True)
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/rnd_demo"

Base: DeclarativeMeta = declarative_base()


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


# metadata object를 만들고 User table을 선언
class UserTable(Base, SQLAlchemyBaseUserTable):
    pass


if __name__ == "__main__":

    engine = sqlalchemy.create_engine(
        DATABASE_URL,
        echo=True
        # connect_args={"check_same_thread": False}
    )

    Base.metadata.create_all(engine)
