#!/usr/bin/python3

from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(cont):
    """teardown app_context"""
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """returns 404...but in json"""
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    host = "0.0.0.0"
    port = "5000"
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT"):
        port = getenv("HBNB_API_PORT")
    app.run(host=host, port=port, threaded=True)
