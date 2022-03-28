#!/usr/bin/python3
"""Pulls up the index of the web application"""
from flask import jsonify, Flask
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """return status of the index if route opens successfully"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats():
    """return number of stats"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
