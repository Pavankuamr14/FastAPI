from fastapi import FastAPI

app=FastAPI()

@app.get('/')
def root():
  return {"message":"welcome to fastapi learning course"}
