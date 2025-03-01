
import psycopg2



import os
base = os.path.dirname(os.path.realpath(__file__))

conn_uri = "host='localhost' dbname='viscord' user='viscord' password='viscord'"

creation_uri = conn_uri
conn = psycopg2.connect(creation_uri)
conn.set_session(autocommit=True)



# with open(os.path.join(base, "CreateDiscordDB.sql")) as f:
    # conn.cursor().execute(f.read())

def connect_to_db():
    conn = psycopg2.connect(conn_uri)
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    return cur

cur = connect_to_db()

