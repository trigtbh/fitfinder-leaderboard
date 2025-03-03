import json
from flask import Response
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


def forbidden():
    return Response(
        json.dumps({"type": "incorrect", "message": "Invalid token"}),
        status=403)