from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
app = FastAPI()
class Post(BaseModel):
  title:str
  context:str
  
  
my_posts=[{'title':"title post 1","content":"content of post 1","id":1},
          {'title':"title post 2","content":"content of post 2","id":2},
          {'title':"favorite food","content":"I like pizza ","id":3}
          ]

@app.get("/")
def root():
    return {"message": "welcome to fastapi learning course"}

@app.get("/posts")
######## THis function will give all posts that currently we are having in the my_posts.
def getposts():
  print(my_posts)
  return my_posts
@app.post("/posts")
# This function is useful for creating an post with tittle and content and with an random value assigning for the id and appending it into our my_post temporary storage variable.
def createpost(post:Post):
  # tempdict={}
  # tempdict['tittle']=post.tittle
  # tempdict['content']=post.context
  # my_posts.append(tempdict)
  post_dict=post.dict()
  post_dict['id']=randrange(1,1000000000000)
  my_posts.append(post_dict)
  return {'data':my_posts}

@app.get("/post/{id}")
# This function will fetch one post.
# id field refers to path parameter.
def getPost(id):
  for d in my_posts:
    if d['id']==int(id):
      
      return {"details":f"your post id is {d['title']}"}
  print(id)
  print(type(id))
  print(type(d['id']))
  print(d['id'])
  return {"details":f"something error is occured and your data is {my_posts}"}