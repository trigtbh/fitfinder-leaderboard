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
from .responses import *

@app.route("/api/users/register", methods=["POST"])
def register():
   
    if not verify(request.json, {"username": str, 
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
    
    if not verify(request.json, {"username": str}):
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



@app.route("/api/users/follow")
def follow():
    if not verify({
        "token": str,
        "other": str,
    }, request.json):
        return invalid_fields()
    
    token = request.json["token"]
    if not is_valid_token(token):
        return forbidden()

    id_ = get_user_id(token)

    cursor.execute(f"""SELECT 1 FROM "{config.META_NAME}"."UserInfo" WHERE id = %s LIMIT 1""", (request.json["other"],))
    exists = cursor.fetchone() is not None 
    
    if not exists: return invalid_fields()

    update_query = f"""
        UPDATE "{config.META_NAME}"."UserInfo"
        SET following_ids = array_append(following_ids, %s)
        WHERE user_id = %s AND NOT (%s = ANY(following_ids));
    """
    try:
        cursor.execute(update_query, (request.json["other"], id_, request.json["other"]))
    except Exception as e:
        return error(e)


    update_query = f"""
        UPDATE "{config.META_NAME}"."UserInfo"
        SET follower_ids = array_append(follower_ids, %s)
        WHERE user_id = %s AND NOT (%s = ANY(follower_ids));
    """
    try:
        cursor.execute(update_query, (id_, request.json["other"], id_))
    except Exception as e:
        return error(e)

    return success()

@app.route("/api/users/unfollow")
def unfollow():
    if not verify({
        "token": str,
        "other": str,
    }, request.json):
        return invalid_fields()
    
    token = request.json["token"]
    if not is_valid_token(token):
        return forbidden()

    id_ = get_user_id(token)

    cursor.execute(f"""SELECT 1 FROM "{config.META_NAME}"."UserInfo" WHERE id = %s LIMIT 1""", (request.json["other"],))
    exists = cursor.fetchone() is not None 

    if not exists:
        return invalid_fields()

    update_query = f"""
        UPDATE "{config.META_NAME}"."UserInfo"
        SET following_ids = array_remove(following_ids, %s)
        WHERE user_id = %s;
    """
    try:
        cursor.execute(update_query, (request.json["other"], id_))
    except Exception as e:
        return error(e)

    update_query = f"""
        UPDATE "{config.META_NAME}"."UserInfo"
        SET follower_ids = array_remove(follower_ids, %s)
        WHERE user_id = %s;
    """
    try:
        cursor.execute(update_query, (id_, request.json["other"]))
    except Exception as e:
        return error(e)

    return success()

@app.route("/api/users/upload_pfp")
def upload_pfp():
    if not verify({
        "token": str,
        "image": str, # base64
    }, request.json):
        return invalid_fields()


    token = request.json["token"]
    if not is_valid_token(token):
        return forbidden()

    id_ = get_user_id(token)

    image_url = "https://cdn.discordapp.com/attachments/1279192010892251207/1345298820719837277/NationalGeographic_2572187_4x3.png?ex=67c40aa9&is=67c2b929&hm=9c3a4061ae809987fa9047ac09b33b702b2aa7e57e7ffc67bbca914e3a054746&"  
    # TODO: connect to S3!


    update_query = f"""
    UPDATE "{config.META_NAME}"."UserInfo"
    SET profile_pic_url = %s
    where id = %s;
    """

    try:
        cursor.execute(update_query, (image_url,))
    except Exception as e:
        return error(e)

    return success()



@app.route("/api/users/followers")
def followers():
    if not verify({
        "token": str
    }, request.json):
        return invalid_fields()
    
    token = request.json["token"]
    if not is_valid_token(token):
        return forbidden()

    id_ = get_user_id(token)
    query = f"""
        SELECT follower_ids
        FROM "{config.META_NAME}"."UserInfo"
        WHERE user_id = %s;
    """
    
    try:
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        data = result[0] if result else []
        return success({"followers": data})
    except Exception as e:
        return error(e)

@app.route("/api/users/following")
def following():
    if not verify({
        "token": str
    }, request.json):
        return invalid_fields()
    
    token = request.json["token"]
    if not is_valid_token(token):
        return forbidden()

    id_ = get_user_id(token)
    query = f"""
        SELECT following_ids
        FROM "{config.META_NAME}"."UserInfo"
        WHERE user_id = %s;
    """
    
    try:
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        data = result[0] if result else []
        return success({"following": data})
    except Exception as e:
        return error(e)


@app.route("/api/users/get")
def getuser():
    if not verify({
        "token": str,
        "other": str,
    }, request.json):
        return invalid_fields()
    
    token = request.json["token"]
    if not is_valid_token(token):
        return forbidden()

    id_ = get_user_id(token)

    cursor.execute(f"""SELECT 1 FROM "{config.META_NAME}"."UserInfo" WHERE id = %s LIMIT 1""", (request.json["other"],))
    exists = cursor.fetchone() is not None 

    if not exists:
        return invalid_fields()


    try:
        cursor.execute(f"""
        select user_id, username, bio_text, profile_pic_url from "{config.META_NAME}"."UserInfo" WHERE id = %s 
        """, request.json["other"])
        result = cursor.fetchone()

        user_id, username, bio, pfp = result

        return success({
            "data": {
                "user_id": user_id,
                "username": username,
                "bio_text": bio,
                "profile_pic_url": pfp 
            }
        })
    except Exception as e:
        return error(e)

