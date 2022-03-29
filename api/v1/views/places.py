#!/usr/bin/python3
"""
Task 9
"""

from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def place(city_id=None):
    """Returns all places or a place by specific ID"""
    if city_id:
        city = storage.get(City, city_id)
        if city is not None:
            placeList = []
            places = storage.all(Place)
            for key, value in places.items():
                if value.city_id == city_id:
                    placeList.append(value.to_dict())
                return jsonify(placeList)
        else:
            abort(404)


@app_views.route("/places/place_id", methods=['GET'],
                 strict_slashes=False)
def place_by_id(place_id=None):
        if place_id:
            place = storage.get(Place, place_id)
            if place:
                return place.to_dict()
            else:
                return abort(404)


@app_views.route("/place/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """deletes a place by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/", methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """add place using POST"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    places = request.get_json()
    if 'user_id' not in places:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user = storage.get(User, place['user_id'])
    if user is None:
        abort(404)
    if 'name' not in places:
        return make_response(jsonify({"error": "Missing name"}), 400)
    place['city_id'] = city_id
    newPlace = Place(**place)
    place.save()
    return make_response(jsonify(newPlace.to_dict()), 201)






@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """update an place using PUT"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    notThese = ["id", "created_at", "updated_at"]
    data = request.get_json()
    for key, value in data.items():
        if key not in notThese:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
