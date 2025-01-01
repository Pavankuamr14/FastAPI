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
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: Optional[str]
    content: Optional[str]

temporaryDataBase = []

def findDataIndex(id_value):
    for index, data in enumerate(temporaryDataBase):
        if data['id'] == id_value:
            return index
    return None

@app.get('/')
def root():
    return {"details": temporaryDataBase}

@app.get('/posts/{id}')
def getdatabyID(id: int):
    for data in temporaryDataBase:
        if data['id'] == id:
            return {"detailed message": data}
    raise HTTPException(status_code=404, detail="Data not found")

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    postData = post.dict()
    postData['id'] = randrange(1, 100000000000)
    temporaryDataBase.append(postData)
    return {"created data": postData}

@app.patch('/posts/{id}')
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
@app.delete('/posts/{id}', status_code=204)
def delete_post(id: int):
    for index, data in enumerate(temporaryDataBase):
        if data['id'] == id:
            del temporaryDataBase[index]  # Safely delete the post
            return {"message": f"Post with ID {id} has been deleted successfully"}
    
    # If no post with the given ID is found
    raise HTTPException(status_code=404, detail="Post not found")