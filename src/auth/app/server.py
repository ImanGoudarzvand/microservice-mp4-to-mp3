from typing import List
from fastapi import FastAPI

server = FastAPI()

@server.get('/')
def home():
    return {"message": "Welcome Home"}
    

