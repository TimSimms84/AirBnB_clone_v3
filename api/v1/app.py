#!/usr/bin/python3
"""Sets up an endpoint to return status of API"""
from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_app(exception):
    """teardown app_context by calling storage.close()"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """returns 404...but in json"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = "0.0.0.0"
    port = '5000'
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT"):
        port = getenv("HBNB_API_PORT")
    app.run(host=host, port=port, threaded=True)
