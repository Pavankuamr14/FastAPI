# from fastapi import FastAPI, status
# from pydantic import BaseModel
# from fastapi.params import Body
# from random import randrange
# from fastapi import HTTPException
# app=FastAPI()
# class Post(BaseModel):
#   title:str
#   content:str


# temporaryDataBase =[]
# def findData(id_value):
#   for data in temporaryDataBase:
#     if data['id']==id_value:
#       return data
# @app.get('/')
# def root():
#   return {"details":temporaryDataBase}

# @app.get('/posts/{id}')
# def getdatabyID(id:int):
#   print(id)
#   print(type(id))
#   Data=findData(id)
#   print(Data)
#   return {"detailed message":f"this is your {Data}"}
#   # return {"detailed message":f"this is your : {Data}"}

# @app.post('/posts',status_code=status.HTTP_201_CREATED)
# def createPost(post: Post):
#   print(post)
#   postData=post.dict()
#   print(postData)
#   postData['id']=randrange(1,100000000000)
#   temporaryDataBase.append(postData)
#   return {"created data":"successful"}

# @app.put('/posts/{id}')
# # put
# def UpdateById(id:int,post:Post):
#   postdata=post.dict()
#   postdata['id']=id
#   data =findData(id)
#   data['id']=id
#   temporaryDataBase[data]=postdata
#   return {'message':f"your are successfuly {postdata}"}


# # from fastapi import FastAPI, status
# # from pydantic import BaseModel
# # from random import randrange

# # app = FastAPI()

# # class Post(BaseModel):
# #     title: str
# #     content: str

# # temporaryDataBase = []

# # @app.get('/')
# # def root():
# #     return {"details": temporaryDataBase}

# # @app.post('/posts', status_code=status.HTTP_201_CREATED)
# # def createPost(post: Post):
# #     print(post)
# #     postData = post.dict()
# #     postData['id'] = randrange(1, 100000000000)
# #     temporaryDataBase.append(postData)
# #     return {"created data": "successful"}

### CURD methods

# C- create
# U - Update
#   PUT
#   PATCH
# R - Read - one post or all post
# D - delete
from fastapi import FastAPI, status, HTTPException, Depends
import psycopg2.extras
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# importing the session from the sqlalchemy
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


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


@app.get("/")
def root():
    return {"details": temporaryDataBase}


# for testing purpose whether connection is done or not
@app.get("/sqlachlemy")
def testing(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return {"data": posts}  # Return the fetched data


@app.get("/posts/{id}")
def getdatabyID(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=404, detail=f"post with id : {id} Data was not found"
        )
    return {"post_details": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(f"{INSERT INTO posts (title,content,published) VALUES (post.title,post.content,post.published)}") --THIS WILL MAY CAUSE THE SQL ingestion TO AVOID THIS WE WILL USE THE BELOW COMMAND

    # cursor.execute(
    #     """INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published
    # )
    # OR #####

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"created data": new_post}


@app.patch("/posts/{id}")
def updatePartialById(id: int, post: Post):
    index = findDataIndex(id)  # Find the index of the post with the given ID
    if index is None:
        raise HTTPException(status_code=404, detail="Data not found")

    # Update only the fields provided in the request
    existing_post = temporaryDataBase[index]
    update_data = post.dict(exclude_unset=True)  # Exclude unset fields
    updated_post = {**existing_post, **update_data}  # Merge existing and update data
    temporaryDataBase[index] = updated_post  # Save back to database

    return {"message": "Successfully updated post", "updated_data": updated_post}


@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # delete_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"pst with id: {id} does not exist",
        )
    post.delete(synchronize_session=False)
    db.commit()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
# put
def UpdateById(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s , published = %s WHERE id = %s RETURNING * """,
    #     (post.title, post.content, post.published, str(id)),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_updated = post_query.first()
    if post_updated == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} is not found ",
        )
    # post_query.update({'title':'hey this is my updated title','content':'this is my updated content'},
    #                   sychronize_session=False)
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
