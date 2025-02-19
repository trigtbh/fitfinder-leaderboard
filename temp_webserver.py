import flask

from listform import Leaderboard, User

lb = Leaderboard()


app = flask.Flask(__name__)

from flask import request


@app.route("/register_bypass", methods=["POST"])
def register_bypass():
    data = request.json

    lb.add(User(data["uuid"], 0))

    return "OK"

@app.route("/update", methods=["POST"])
def update():
    data = request.json

    lb.update(data["uuid"], data["score"])

    return "OK"

@app.route("/score", methods=["POST"])
def score():
    data = request.json

    return str(lb.score(data["uuid"]))

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

    user = lb.get_user(data["uuid"])
    score = user.score + data["increment"]
    lb.update(data["uuid"], score)


@app.route("/placement", methods=["POST"])
def placement():
    data = request.json

    return str(lb.placement(data["uuid"]))

@app.route("/", methods=["GET"])
def index():
    return "This server is part of an ongoing stress test for Fitfinder."


if __name__ == "__main__":
    app.run(port=5002, debug=True)