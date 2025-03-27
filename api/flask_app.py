from flask import Flask

app = Flask(__name__)

from . import debug
debug.loaded(__name__)