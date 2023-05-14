from fastapi import FastAPI 
from pymongo import MongoClient
import os

# MONGO_URI = "mongodb://host.minikube.internal:27017"
MONGODB_HOST = os.environ["MONGODB_HOST"]
MONGODB_PORT = os.environ["MONGODB_PORT"]
MONGO_URI = f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}"

client = MongoClient(MONGO_URI)
db_videos = client['videos']
db_mp3s = client['mp3s']

