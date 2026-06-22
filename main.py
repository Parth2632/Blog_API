from fastapi import FastAPI
from database import engine 
import models 

models.Base.metadata.create_all(bind=engine) #create a table

app = FastAPI()

@app.get("/")
def home():
    return{
        "Message": "Welcome to Blog API"
    }

