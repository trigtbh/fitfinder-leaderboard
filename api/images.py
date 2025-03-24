import datetime
from .db import cur
from .login_flow import tokens
from typing import Literal
from uuid import uuid4
from json import dumps
import random
from .helpers import *
from .flask_app import app
from flask import request, Response, send_file
import requests
from .config import URI
import hashlib
from .responses import *
from . import config
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import base64
from io import BytesIO

uri = os.getenv("MONGO_URI") # load_dotenv() has to be called before this!
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["Aura"]["images"]

@app.route("/i/create", methods=["POST"])
def upload_image():
    if request.remote_addr != "127.0.0.1":
        return Response(status=404)

    db.insert_one(request.json)
    return "OK"

@app.route("/i/<post:post>")
def get_image(post: str):
    data = db.find_one({"_id": post})
    if not data: return Response(status=404)

    img = data["contents"]
    img_data = base64.b64decode(img)
    img_stream = io.BytesIO(img_data)
    return send_file(img_stream, mimetype="image/png")
