from dotenv import load_dotenv
load_dotenv()

from api import config, db, leaderboard, login_flow, posts, responses, tags, users, images

from validate import get_key

key = get_key()

users.register_key(key)
login_flow.register_key(key)


from api.flask_app import app

@app.route("/")
def index():
    return "Aura server running! 🧡"

if __name__ == "__main__":
    print("Validation succeeded.")
