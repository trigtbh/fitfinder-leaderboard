import json
from flask import Response
from .login_flow import tokens
import requests
from .config import URI 

def invalid_fields():
    return Response(
        json.dumps({"type": "incorrect", "message": "Invalid fields"}),
        status=400)

def error(e):
    print("Request error: " + str(e))
    return Response(
        json.dumps({"type": "error", "message": str(e)}),
        status=500)

def success(data={}):
    return Response(
        json.dumps({"type": "success"} | data),
        status=200)

def missing_permissions():
    return Response(
        json.dumps({"type": "incorrect", "message": "You do not have permission to perform this action"}),
        status=403)

def is_valid_token(token: str) -> bool:
    return token in tokens

def get_user_id(token: str) -> str:
    name, _id = tokens[token]
    return _id

def forbidden():
    return Response(
        json.dumps({"type": "incorrect", "message": "Invalid token"}),
        status=403)