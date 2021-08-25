import os
import sys

sys.path.append("c:\\projects\\fastapi-demo")
print(sys.path)
import databases
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.dev.env", verbose=True)

from typing import Optional

from fastapi import FastAPI

from appUsers.routes import auth

# get environments
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/rnd_demo"

database = databases.Database(DATABASE_URL)


app = FastAPI()
app.include_router(auth.get_users_router(), tags=["Authentication"], prefix="/api")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
