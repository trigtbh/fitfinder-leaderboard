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
from . import config
from .db import mongo_client

@app.route("/posts/upload", methods=["POST"])
def upload():
    if not verify({
        "token": str,
        "image": str, # base64
        "caption": str
    }, request.json):
        return invalid_fields()


    token = request.json["token"]
    if not is_valid_token(token):
        return forbidden()

    id_ = get_user_id(token)

    post_id = str(uuid4())

    #image_url = "https://cdn.discordapp.com/attachments/1279192010892251207/1345298820719837277/NationalGeographic_2572187_4x3.png?ex=67c40aa9&is=67c2b929&hm=9c3a4061ae809987fa9047ac09b33b702b2aa7e57e7ffc67bbca914e3a054746&" 
    # TODO: connect above image url with S3. maybe have someone else do this!

    # TODO: connect with the /images/upload endpoint?!

    resp = requests.post("/i/create", json={
        "_id": id_,
        "contents": request.json["image"]

    })

    image_url = config.PUBLIC_URI + "/i/" + id_

    query = f"""insert into "{config.META_NAME}"."postinfo"
    (post_id, user_id, image_url, post_caption, time_created)
    values (%s, %s, %s, %s, %s)"""
    try:
        cur.execute(query, (post_id, id_, image_url, request.json["caption"], datetime.datetime.now()))
        return success()
    except Exception as e:
        return error(e)


@app.route("/posts/like", methods=["POST"])
def like():
    if not verify({
        "token": str,
        "post_id": str
    }, request.json):
        return invalid_fields()

    token = request.json["token"]
    if not is_valid_token(token):
        return forbidden()

    id_ = get_user_id(token)

    cur.execute(f"""SELECT 1 FROM "{config.META_NAME}"."postinfo" WHERE id = %s LIMIT 1""", (request.json["post_id"],))
    exists = cur.fetchone() is not None 
    
    if not exists: return invalid_fields()


    cur.execute(f"""SELECT user_id FROM "{config.META_NAME}"."postinfo" WHERE id = %s LIMIT 1""", (request.json["post_id"],))
    author_id = cur.fetchone()[0]

    requests.post(config.URI + "/leaderboard/increment", json={
        "id": author_id,
        "increment": 1
    })




    like_id = str(uuid4())

    insert_query = f"""
    insert into "{config.META_NAME}"."like_info"
    (like_id, user_liked, like_timestamp) 
    values (%s, %s, %s)
    """

    try:
        cur.execute(insert_query, (like_id, id_, datetime.datetime.now()))
    except Exception as e:
        return error(e)



    update_query = f"""
        UPDATE "{config.META_NAME}"."postinfo"
        SET likes = array_append(likes, %s)
        WHERE post_id = %s AND NOT (%s = ANY(likes));
    """
    try:
        cur.execute(update_query, (like_id, request.json["post_id"], like_id))
        return success()
    except Exception as e:
        return error(e)


@app.route("/posts/unlike", methods=["POST"])
def unlike():
    if not verify({
        "token": str,
        "post_id": str
    }, request.json):
        return invalid_fields()

    token = request.json["token"]
    if not is_valid_token(token):
        return forbidden()

    id_ = get_user_id(token)

    cur.execute(f"""SELECT 1 FROM "{config.META_NAME}"."postinfo" WHERE id = %s LIMIT 1""", (request.json["post_id"],))
    exists = cur.fetchone() is not None

    if not exists:
        return invalid_fields()

    requests.post(config.URI + "/leaderboard/increment", json={
        "id": id_,
        "increment": -1
    })


    cur.execute(f"""SELECT like_id FROM "{config.META_NAME}"."postinfo" 
    WHERE user_liked = %s AND like_id = ANY(
        SELECT unnest(likes) FROM "{config.META_NAME}"."postinfo" WHERE id = %s)""", (id_, request.json["post_id"]))
    
    like_record = cur.fetchone()
    if not like_record:
        return invalid_fields()

    like_id = like_record[0]

    delete_query = f"""
    DELETE FROM "{config.META_NAME}"."like_info"
    WHERE like_id = %s;
    """

    try:
        cur.execute(delete_query, (like_id,))
    except Exception as e:
        return error(e)

    update_query = f"""
        UPDATE "{config.META_NAME}"."postinfo"
        SET likes = array_remove(likes, %s)
        WHERE post_id = %s;
    """
    try:
        cur.execute(update_query, (like_id, request.json["post_id"]))
        return success()
    except Exception as e:
        return error(e)



@app.route("/posts/comment", methods=["POST"])
def comment():
    if not verify({
        "token": str,
        "post_id": str,
        "comment": str
    }, request.json):
        return invalid_fields()

    token = request.json["token"]
    if not is_valid_token(token):
        return forbidden()

    id_ = get_user_id(token)

    cur.execute(f"""SELECT 1 FROM "{config.META_NAME}"."postinfo" WHERE id = %s LIMIT 1""", (request.json["post_id"],))
    exists = cur.fetchone() is not None 
    
    if not exists: return invalid_fields()

    comment_id = str(uuid4())

    insert_query = f"""
    insert into "{config.META_NAME}"."comment_info"
    (comment_id, comment_text, user_commented, comment_timestamp) 
    values (%s, %s, %s, %s)
    """

    try:
        cur.execute(insert_query, (comment_id, requests.json["comment"], id_, datetime.datetime.now()))
    except Exception as e:
        return error(e)


    update_query = f"""
        UPDATE "{config.META_NAME}"."postinfo"
        SET likes = array_append(likes, %s)
        WHERE post_id = %s;
    """
    try:
        cur.execute(update_query, (comment_id, request.json["post_id"]))
        return success()
    except Exception as e:
        return error(e)

viewed = {}

@app.route("/posts/next")
def nextpost():
    if not verify({
        "token": str
    }, request.json):
        return invalid_fields()

    token = request.json["token"]
    if not is_valid_token(token):
        return forbidden()

    id_ = get_user_id(token)

    if id_ not in viewed:
        viewed[id_] = set()

    
    id_ = get_user_id(token)
    query = f"""
        SELECT post_id
        FROM "{config.META_NAME}"."postinfo"
    """
    
    try:
        cur.execute(query, (id_,))
        result = cur.fetchone()
        data = result[0] if result else []
    except Exception as e:
        return error(e)

    data = set(data)

    valid = data - viewed[id_]

    if len(valid) == 0:
        return error("no new posts")

    new = valid.pop()

    viewed[id_].add(new)

    return success({"data": new})


from . import debug
debug.loaded(__name__)