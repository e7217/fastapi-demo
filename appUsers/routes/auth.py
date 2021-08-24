import os, sys
# sys.path.append('c:\\projects\\he-be-fastapi')
# print(sys.path)

import databases
import sqlalchemy
from fastapi import Form, HTTPException, APIRouter, Depends, status
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from appUsers.models.users import User, UserCreate, UserUpdate, UserDB, UserTable

from dotenv import load_dotenv
load_dotenv(dotenv_path='../.dev.env', verbose=True)
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/rnd_demo"

database = databases.Database(DATABASE_URL)

Base: DeclarativeMeta = declarative_base()

users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)

router = APIRouter(prefix="/auth")