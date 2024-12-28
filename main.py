from fastapi import FastAPI

app=FastAPI()

@app.get('/')
def root():
  return {"message":"welcome to fastapi learning course"}

########################
@app.get('/')
def demo():
  return {"message":"This is first msg need to be display"}

#############################
@app.get('/login')
def loginfunction():
  return {"Message":"welcome to login route page.."}
