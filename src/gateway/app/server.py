from fastapi import FastAPI, Request, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
import gridfs, pika
from .schemas import UserCreate, UserLogin
from .database import db_mp3s, db_videos
from app.storage import utils
from app.auth_svc import access, registery
from app.auth import validate
from bson.objectid import ObjectId
from app.jwt.jwt_bearer import JWTBearer
import json
# from app.middlewares.basic_authentication import BasicAuthBackend
    

server = FastAPI()

fs_videos = gridfs.GridFS(db_videos)
fs_mp3s = gridfs.GridFS(db_mp3s)


# connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq-service"))

channel = connection.channel()


# @app.get("/")
# def home(request: Request):

#     return {"message": "gateway app running"}


@server.post("/signup")
def signup(request: Request, user: UserCreate):

    response, err = registery.register(user)

    if not err:
        return json.loads(response)
    
    err_message, err_status_code = err

    err_message = json.loads(err_message)
    raise HTTPException(err_status_code, err_message["detail"]) 


@server.post("/login")
def login(user: UserLogin):

    token, err = access.login(user)

    if not err:
        return json.loads(token)
    
    err_message, err_status_code = err

    err_message = json.loads(err_message)
    raise HTTPException(err_status_code, err_message["detail"]) 


@server.post("/upload", dependencies=[Depends(JWTBearer())])
def upload(request: Request, file: UploadFile):

    access, error = validate.token(request)
    if not access:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    access = json.loads(access) # from str to python dict 

    err =  utils.upload(file.file, fs_videos, channel, access["payload"])

    if err:
        return err

    return "success!", 200
    # return {"OK"}


@server.get("/download")
def download(request: Request, fid: str):
    return {"pass"}

