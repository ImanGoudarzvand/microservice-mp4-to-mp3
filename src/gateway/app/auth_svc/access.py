import os, requests
from fastapi import FastAPI, Request
import json 
from app.schemas import UserLogin

def login(user: UserLogin):



    # response = requests.post(f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login", auth = basicAuth)
    user = dict(user)
    # response = requests.post(f"http://192.168.49.2:30013/login", data = json.dumps(user))
    response = requests.post(f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login", data = json.dumps(user))

    if response.status_code == 200:
        return response.text, None
        
    return None, (response.text, response.status_code) 