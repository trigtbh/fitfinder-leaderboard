from api import config, db, leaderboard, login_flow, posts, responses, tags, users

from api.flask_app import app

@app.route("/")
def index():
    return "Aura server running! 🧡"

if __name__ == "__main__":
    print("Validation succeeded.")