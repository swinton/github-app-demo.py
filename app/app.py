import flask

from flask import request


app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    print request.get_json()
    return "Hello {}!".format("world")
