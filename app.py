import os, sys

from api import debug

debug.clear()

if "gunicorn" in sys.argv[0]:
    os.environ["aura_env"] = "prod"
else:
    os.environ["aura_env"] = "dev"

import logging

log = logging.getLogger('werkzeug')
log.disabled = True



debug.info("Starting Aura server...")
debug.info("Environment: " + debug.term.bold + debug.term.blue + os.environ["aura_env"] + debug.term.normal)



from dotenv import load_dotenv
load_dotenv()

from api import config, db, leaderboard, login_flow, posts, responses, tags, users, images

from validate import get_key

key = get_key()

debug.info("Key validation successful.")
users.register_key(key)
login_flow.register_key(key)


from api.flask_app import app

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

@app.route("/")
def index():
    return "Aura server running! 🧡"

debug.success("Server up!")

if __name__ == "__main__":
    if os.environ["aura_env"] == "dev":
        try:
            app.run(host="0.0.0.0", port=5000)
        except KeyboardInterrupt:
            debug.info("Shutting down...")
            exit(0)