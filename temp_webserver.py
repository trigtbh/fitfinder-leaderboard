import flask

from listform import Leaderboard, User

lb = Leaderboard()


app = flask.Flask(__name__)

from flask import request


# import redis, pickle, sys

# redis_client = redis.Redis(host="127.0.0.1", port=6379, db=0)

# def get_shared_object():
#     obj_data = redis_client.get("leaderboard")
#     if obj_data:
#         return pickle.loads(obj_data)
#     return None

# def set_shared_object(obj):
#     redis_client.set("leaderboard", pickle.dumps(obj))

# lb: Leaderboard = get_shared_object()
# if not lb or (len(sys.argv) > 1 and sys.argv[1] == "reset"):
#     print("resetting leaderboard")
#     lb = Leaderboard()
#     set_shared_object(lb)

# del lb




@app.route("/register_bypass", methods=["POST"])
def register_bypass():
    data = request.json
    lb.insert(data["uuid"])
    set_shared_object(lb)
    return "OK"

@app.route("/update", methods=["POST"])
def update():
    data = request.json
    
    lb.update(data["uuid"], data["score"])
    set_shared_object(lb)
    return "OK"

@app.route("/score", methods=["POST"])
def score():
    data = request.json
    
    return str(lb.get(data["uuid"]))

@app.route("/adjacent", methods=["POST"])
def adjacent():
    data = request.json
    
    return str(lb.adjacent(data["uuid"]))

@app.route("/top_ten", methods=["GET"])
def top_ten():
    
    return str(lb.top_ten())

@app.route("/increment", methods=["POST"])
def increment():
    data = request.json
    
    score = lb.get(data["uuid"]) + data["increment"]
    lb.update(data["uuid"], score)
    set_shared_object(lb)
    return "OK"


@app.route("/placement", methods=["POST"])
def placement():
    data = request.json
    
    return str(lb.placement(data["uuid"]))

@app.route("/", methods=["GET"])
def index():
    return "This server is part of an ongoing stress test for Fitfinder."


if __name__ == "__main__":
    app.run(port=5003, debug=True)