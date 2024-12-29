from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
  tittle:str
  context:str
@app.get("/")
def root():
    return {"message": "welcome to fastapi learning course"}


########################
@app.get("/")
def demo():
    return {"message": "This is first msg need to be display"}


#############################
@app.get("/login")
def loginfunction():
    return {"Message": "welcome to login route page.."}


# @app.post("/createPost")
# def createpost():
#     return {"New_user": "newuser is successfully created"}


# @app.post('/createPost')
# def createpost(payloads:dict =Body(...)):
#   print(payloads)

#   return {"New_Post":f"{payloads['tittle']} New_Post is created successfully And content is {payloads['context']}"}
@app.post('/createPost')
def createpost(New_Post:Post):
  print(payloads)

  return {"New_Post":f"{payloads['tittle']} New_Post is created successfully And content is {payloads['context']}"}
