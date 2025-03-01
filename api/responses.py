from flask import Response

def success(data):
    return Response(status=200)