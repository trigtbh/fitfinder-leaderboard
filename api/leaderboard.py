import datetime
from .db import cur
from .login_flow import tokens
from typing import Literal
from json import dumps
import random
from .helpers import *
from .flask_app import app
from flask import request, Response
import requests
from .config import URI
import hashlib
from .responses import *


from .dbform import Leaderboard, User

lb = Leaderboard()

from flask import request

@app.route("/leaderboard/update", methods=["POST"])
def update():
    if request.remote_addr != "127.0.0.1": return forbidden()
    if not verify(request.json, {"id": str, "score": int}): 
        return invalid_fields()

    data = request.json
    lb.update(data["id"], data["score"])
    return "OK"

@app.route("/leaderboard/score")
def score():
    if not verify(request.json, {"id": str}): 
        return invalid_fields()

    data = request.json
    return str(lb.get(data["id"]))

@app.route("/leaderboard/adjacent", methods=["POST"])
def adjacent():
    if not verify(request.json, {"id": str}): 
        return invalid_fields()

    data = request.json
    return str(lb.adjacent(data["id"]))

@app.route("/leaderboard/top_ten")
def top_ten():
    return str(lb.top_ten())

@app.route("/leaderboard/increment", methods=["POST"])
def increment():
    if request.remote_addr != "127.0.0.1": return forbidden()
    if not verify(request.json, {"id": str, "increment": int}): 
        return invalid_fields()

    data = request.json
    score = lb.get(data["id"]) + data["increment"]
    lb.update(data["id"], score)
    return "OK"

@app.route("/leaderboard/placement")
def placement():
    if not verify(request.json, {"id": str}): 
        return invalid_fields()

    data = request.json
    return str(lb.placement(data["id"]))

from . import debug
debug.loaded(__name__)