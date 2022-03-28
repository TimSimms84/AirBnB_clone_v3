#!/usr/bin/python3
"""
Task 7
"""

import re
from flask import jsonify, request, make_response, abort
# from api.v1.app import page_not_found
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route("/states", methods=['GET'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def states(state_id=None):
    """Returns all states or a state by specific ID"""
    if state_id:
        obj = storage.get(State, state_id)
        if obj is not None:
            return obj.to_dict()
        else:
            return abort(404)
    else:
        states = storage.all(State)
        statelist = []
        for state in states.values():
            statelist.append(state.to_dict())
        return jsonify(statelist)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def state_delete(state_id):
    """deletes a state by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route("/states/", methods=['POST'], strict_slashes=False)
def post_state():
    """add state using POST"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing Name"}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """update a state using PUT"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    notThese = ["id", "created_at", "updated_at"]
    data = request.get_json()
    for key, value in data.items():
        if key not in notThese:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 400)
