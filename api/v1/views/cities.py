#!/usr/bin/python3
"""Task 8"""


from flask import jsonify, request, make_response, abort
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


# @app_views.route("/cities", methods=['GET'], strict_slashes=False)
@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def cities_list(state_id=None):
    """Returns all cities or a single city by State ID"""
    if state_id:
        obj = storage.get(State, state_id)
        if obj is not None:
            cities_list = []
            for city in obj.cities:
                cities_list.append(city.to_dict())
            return jsonify(cities_list)
        else:
            return abort(404)
    else:
        return abort(404)

@app_views.route("/cities/<city_id>", methods=['GET'])
def city_by_id(city_id):
    if city_id:
        city = storage.get(City, city_id)
        if city is None:
            return abort(404)
        return city.to_dict()



@app_views.route("/cities/<city_id>", methods=['DELETE'])
def city_delete(city_id):
    """deletes a state by ID"""
    if city_id:
        obj = storage.get(City, city_id)
        if obj is not None:
            storage.delete(obj)
            storage.save()
            return jsonify({})
        else:
            return abort(404)


@app_views.route("/states/<state_id>/cities/", methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """add state using POST"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing Name"}), 400)
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    cities = request.get_json()
    cities['state_id'] = state_id
    city = City(**cities)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """update a state using PUT"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    notThese = ["id", "created_at", "updated_at"]
    data = request.get_json()
    for key, value in data.items():
        if key not in notThese:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict())
