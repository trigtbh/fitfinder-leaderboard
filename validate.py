import requests
import os

import dotenv, hashlib
dotenv.load_dotenv()

for key in [
    "VALIDATION_SERVER",
    "VALIDATION_HASH"
]:
    if key not in os.environ:
        print(f"Missing environment variable: {key}")
        exit(1)

url = os.environ["VALIDATION_SERVER"]
hash_ = os.environ["VALIDATION_HASH"]

import cloudpickle

def get_key():
    resp = requests.get(url + "/key", stream=True, verify=True)
    if hashlib.sha256(resp.raw.connection.sock.getpeercert(binary_form=True)).hexdigest() != hash_:
        print("Invalid server certificate.")
        exit(1)

    return cloudpickle.loads(resp.content).key()