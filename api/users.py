import datetime
from .db import cur
from .login_flow import tokens
from typing import Literal
from uuid import uuid4
from json import dumps
import random
from .helpers import *
from .flask_app import app
from flask import request, Response
import requests
from .config import URI
import hashlib

@app.route("/api/users/register", methods=["POST"])
def register():
   
    if not validate_fields(request.json, {"username": str, 
    "password": str, "full_name": str, "email": str, "phone_number": str}):
        return invalid_fields()

    user_id = str(uuid4())
    username = request.json["username"]
    full_name = request.json["full_name"]
    email = request.json["email"]
    phone = request.json["phone_number"]

    user_id = uuid4()
    
    password = hashlib.sha256(request.json["password"].encode()).hexdigest()
    



    resp = requests.post(URI + "/api/users/check_username", json={"username": username})
    if resp.status_code != 200:
        return error("Failed to check username availability")
    if not resp.json()["available"]:
        return error(f"Username is already taken")




    send_query=f'''
    insert into "{config.META_NAME}"."UserInfo" 
    (user_id, username, password_hash, full_name, email, phone_number) 
    values (%s, %s, %s, %s, %s, %s)
    '''
    try:
        cur.execute(send_query, (user_id, username, password, full_name, email, phone))
        return success()
    except Exception as e:
        return error(e)




@app.route("/api/users/check_username", methods=["POST"])
def username_available():
    
    if not validate_fields(request.json, {"username": str}):
        return invalid_fields()
    
    username = request.json["username"]

    send_query = f"""select 1 from "{config.META_NAME}"."UserInfo" where username = %s"""
    try:
        cur.execute(send_query, (username,)) # weird tuple hack
        records = cur.fetchall()
        data = {"available": len(records) == 0}
        return Response(dumps(data), status=200, mimetype="application/json")
    except Exception as e:
        return error(e)