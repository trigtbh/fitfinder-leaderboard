
import psycopg2
import dotenv
from . import debug
dotenv.load_dotenv()


import os, sys
base = os.path.dirname(os.path.realpath(__file__))

if os.environ["aura_env"] == "prod":
    conn_uri = os.getenv("DB_PROD")
else:
    conn_uri = os.getenv("DB_DEV")

creation_uri = conn_uri
try:
    conn = psycopg2.connect(creation_uri)
except:
    debug.error("Failed to connect to database.")
conn.set_session(autocommit=True)




# with open(os.path.join(base, "CreateDiscordDB.sql")) as f:
    # conn.cursor().execute(f.read())

def connect_to_db():
    conn = psycopg2.connect(conn_uri)
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    return cur

cur = connect_to_db()

if os.environ["aura_env"] == "dev":
    wipe = debug.warning_yn("You are running the development version. Wipe development database?")

    if wipe:
        base = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        with open(os.path.join(base, "utils", "wipe_db.sql")) as f:
            cur.execute(f.read())

import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import dotenv
dotenv.load_dotenv()

mongo_uri = os.getenv("MONGO_URI") # load_dotenv() has to be called before this!
mongo_client = MongoClient(mongo_uri, server_api=ServerApi('1'))


from . import debug
debug.loaded(__name__)