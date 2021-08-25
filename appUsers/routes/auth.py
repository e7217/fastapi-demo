import os
import sys
from typing import Any, Callable, Dict, Optional, Sequence, Type

import databases
import sqlalchemy
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from appUsers.models.users import User, UserCreate, UserDB, UserTable, UserUpdate

# sys.path.append('c:\\projects\\he-be-fastapi')
# print(sys.path)


# get environments
load_dotenv(dotenv_path="../.dev.env", verbose=True)
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/rnd_demo"
SECRET = os.getenv("SECRET")

# database
database = databases.Database(DATABASE_URL)
Base: DeclarativeMeta = declarative_base()
users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)

# JWT
auth_backends = []
jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="auth/jwt/login"
)
auth_backends.append(jwt_authentication)

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)


def get_users_router():
    users_router = APIRouter()

    def on_after_register(user: UserDB, request: Request):
        print(f"User {user.id} has registered.")

    def on_after_forgot_password(user: UserDB, token: str, request: Request):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    def on_after_reset_password(user: UserDB, request: Request):
        print(f"User {user.id} has reset their password.")

    def on_after_update(
        user: UserDB, updated_user_data: Dict[str, Any], request: Request
    ):
        print(
            f"User {user.id} has been updated with the following data: {updated_user_data}"
        )

    def on_after_verification_request(user: UserDB, token: str, request: Request):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    users_router.include_router(
        fastapi_users.get_auth_router(jwt_authentication),
        prefix="/auth/jwt",
    )
    users_router.include_router(
        fastapi_users.get_register_router(on_after_register),
        prefix="/auth",
    )
    users_router.include_router(
        fastapi_users.get_reset_password_router(
            SECRET,
            after_forgot_password=on_after_forgot_password,
            after_reset_password=on_after_reset_password,
        ),
        prefix="/auth",
    )
    users_router.include_router(
        fastapi_users.get_users_router(on_after_update),
        prefix="/auth",
    )
    users_router.include_router(
        fastapi_users.get_verify_router(
            SECRET, after_verification_request=on_after_verification_request
        ),
        prefix="/auth",
    )

    return users_router
