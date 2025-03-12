from .db import cur
from cryptography.fernet import Fernet
from .responses import *
import os
from uuid import uuid4

from flask import request, Response
from .flask_app import app

from . import config

import json

import hashlib

key = os.getenv("FF_KEY")
if not key:
    key = Fernet.generate_key()
    os.system("export FF_KEY=" + key.decode())
else:
    key = key.encode()

base_path = os.path.basename(os.path.basename(os.path.realpath(__file__)))

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


tokens = {}

from .fastcrypt import encrypt

global extra_key
extra_key = ""

def register_key(key):
    global extra_key
    extra_key = key


@app.route("/login", methods=["POST"])
def handle_login():
    if not verify(request.json, {"username": str, "password": str, "sys_uuid": str}): 
        return invalid_fields()

    user = request.json["username"]

    password = hashlib.sha256(request.json["password"].encode()).hexdigest()
    password = encrypt(password, extra_key)
    
    sys_uuid = request.json["sys_uuid"]

    send_query = f"""select user_id, username from {config.META_NAME}."UserInfo" where username = %s and user_password = %s"""
    try:
        cur.execute(send_query, (user, password))
        records = cur.fetchall()
        if len(records) > 0:
            token = str(uuid4())
            tokens[token] = (user, records[0][0])
            f = Fernet(key + str(sys_uuid).encode())
            cache = f.encrypt(token.encode("utf-8")).decode("utf-8")

            d = {"type": "success", "token": token, "cache": cache, "user_id": records[0][0], "username": records[0][1]}
            return Response(json.dumps(d), status=200)
        else:
            d = {"type": "invalid", "message": "Invalid credentials"}
            return Response(json.dumps(d), status=403)
    except Exception as e:
        return Response(json.dumps({"type": "error", "message": str(e)}), status=500)


@app.route("/login/bypass", methods=["POST"])
def handle_token_bypass():
    if not verify(request.json, {"cache": str, "sys_uuid": str}):
        return invalid_fields()
    
    cache = request.json["cache"]
    sys_uuid = request.json["sys_uuid"]

    try:
        f = Fernet(key + str(sys_uuid).encode())
        token = f.decrypt(cache.encode("utf-8")).decode("utf-8")

        name, _id = tokens[token]
        query = f"""select user_id, username from {config.META_NAME}."UserInfo" where username = %s"""
        cur.execute(query, (name,))
        records = cur.fetchall()
        if len(records) == 0:
            return Response(json.dumps({"type": "invalid", "message": "Invalid token"}), status=403)
        d = {"type": "success", "token": token, "user_id": records[0][0], "username": records[0][1]}
        return Response(json.dumps(d), status=200)
    except Exception as e:
        return Response(json.dumps({"type": "error", "message": str(e)}), status=500)
    


from .helpers import *