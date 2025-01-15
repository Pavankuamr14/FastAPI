from fastapi import FastAPI, status, HTTPException, Depends
import psycopg2.extras
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="pavan@5701",
            cursor_factory=psycopg2.extras.RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print("connection to database error")
        print("Error: ", error)
        time.sleep(2)


temporaryDataBase = [{"title": "first title", "content": "my first post title", id: 1}]


def findDataIndex(id_value):
    for index, data in enumerate(temporaryDataBase):
        if data["id"] == id_value:
            return index
    return None


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"data": "welcome page..."}
