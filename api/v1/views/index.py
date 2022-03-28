#!/usr/bin/python3
"""Pulls up the index of the web application"""
from flask import jsonify, Flask
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """return status of the index if route opens successfully"""
    return jsonify({"status": "OK"})


# @app_views.route('/stats', methods=['GET'])
# def stats():
#     """return number of stats"""
#     return jsonify({"amenities": storage.count("Amenity"),
#                     "cities": storage.count("City"),
#                     "places": storage.count("Place"),
#                     "reviews": storage.count("Review"),
#                     "states": storage.count("State"),
#                     "users": storage.count("User")})

@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats():
    """ returns dictionary with classes and their count"""
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    countDict = {}
    for objType, cls in classes.items():
        countDict.update({objType: storage.count(cls)})
    return jsonify(countDict)
