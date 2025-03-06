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


@app.route("/api/tags/add")
def add_tag():
    if not verify({
        "token": str,
        "tag_id": str, # base64
    }, request.json):
        return invalid_fields()


    token = request.json["token"]
    if not is_valid_token(token):
        return forbidden()

    id_ = get_user_id(token)

    query = f"""
        SELECT all_tag_ids 
        FROM "{config.META_NAME}"."UserInfo"
        WHERE user_id = %s;
    """
    
    try:
        cur.execute(query, (id_,))
        result = cur.fetchone()
        data = result[0] if result else []
    except Exception as e:
        return error(e)

    if request.json["tag_id"] not in data:
        return forbidden()


    update_query = f"""
        UPDATE "{config.META_NAME}"."UserInfo"
        SET profile_tag_ids = array_append(profile_tag_ids, %s)
        WHERE user_id = %s AND NOT (%s = ANY(profile_tag_ids));
    """
    try:
        cur.execute(update_query, (id_, request.json["tag_id"], id_))
    except Exception as e:
        return error(e)

    return success()

    
@app.route("/api/tags/remove")
def remove_tag():
    if not verify({
        "token": str,
        "tag_id": str, # base64
    }, request.json):
        return invalid_fields()


    token = request.json["token"]
    if not is_valid_token(token):
        return forbidden()

    id_ = get_user_id(token)

    query = f"""
        SELECT profile_tag_ids 
        FROM "{config.META_NAME}"."UserInfo"
        WHERE user_id = %s;
    """
    
    try:
        cur.execute(query, (id_,))
        result = cur.fetchone()
        data = result[0] if result else []
    except Exception as e:
        return error(e)

    if request.json["tag_id"] not in data:
        return forbidden()


    update_query = f"""
        UPDATE "{config.META_NAME}"."UserInfo"
        SET profile_tag_ids = array_remove(profile_tag_ids, %s)
        WHERE user_id = %s;
    """
    try:
        cur.execute(update_query, (id_, request.json["tag_id"]))
    except Exception as e:
        return error(e)

    return success()

    
    
    


@app.route("/api/tags/get")
def get_tags():
    if not verify({
        "token": str
    }, request.json):
        return invalid_fields()
    
    token = request.json["token"]
    if not is_valid_token(token):
        return forbidden()

    id_ = get_user_id(token)
    query = f"""
        SELECT all_tag_ids
        FROM "{config.META_NAME}"."UserInfo"
        WHERE user_id = %s;
    """
    
    try:
        cur.execute(query, (id_,))
        result = cur.fetchone()
        data = result[0] if result else []
        return success({"followers": data})
    except Exception as e:
        return error(e)
