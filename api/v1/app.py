#!/usr/bin/python3
"""Task 6"""
from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint
from models import storage
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(cont):
    """teardown app_context"""
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
