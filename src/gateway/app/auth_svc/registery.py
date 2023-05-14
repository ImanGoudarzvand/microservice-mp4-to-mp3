import os, requests
from fastapi import FastAPI, Request
from app.schemas import UserCreate
import json

def register(user: UserCreate):


    # response = requests.post(f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/signup",
    #                          body = json.dumps(user))
#     # print(os.environ.get('AUTH_SVC_ADDRESS'))
    user = dict(user)
    # response = requests.post(f"http://192.168.49.2:30013/signup", data = json.dumps(user))
    response = requests.post(f"{os.environ.get('AUTH_SVC_ADDRESS')}/signup", data = json.dumps(user))

    if response.status_code == 200:
        return response.text, None

    return None, (response.text, response.status_code) 