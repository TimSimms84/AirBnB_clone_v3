#!/usr/bin/python3
"""Task 8"""

from flask import jsonify
from api.v1.app import page_not_found
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage
from requests import request

@app_views.route("/cities", methods=['GET'], strict_slashes=False)
@app_views.route("/states/<state_id>/cities", methods=['GET'], strict_slashes=False)
def cities_list(state_id=None):
    """Returns all cities or a single city by State ID"""

    if state_id:
        obj = storage.get(City, state_id)
        if obj is not None:
            return obj.to_dict()
        else:
            return page_not_found(404)
    else:
        citys = storage.all(City)
        citylist = []
        for city in citys.values():
            citylist.append(city.to_dict())
        return jsonify(citylist)

@app_views.route("/cities/<city_id>", methods=['DELETE'])
def city_delete(city_id):
    """deletes a state by ID"""
    if city_id:
        obj = storage.get(City, city_id)
        if obj is not None:
            storage.delete(obj)
        else:
            return page_not_found(404)

@app_views.route("/states/<state_id>/cities", methods=['POST'], strict_slashes=False)
def city_post(state_id, city_id):
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}, 400)
    if state_id:
        obj = storage.get(State, state_id)
        if obj is not None:
            storage.get(obj)
        else:
            return page_not_found(404)
        if city_id:
            _obj = storage.get(City, city_id)
            if _obj is not None:
                storage.get(_obj)
            else:
                return page_not_found(404)

@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def city_put(city_id):
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}, 400)
    if city_id:
        obj = storage.get(City, city_id)
        if obj is not None:
            storage.get(obj)
        else:
            return page_not_found(404)
