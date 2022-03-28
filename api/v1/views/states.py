#!/usr/bin/python3
"""
Task 7
"""

from flask import jsonify
from api.v1.app import page_not_found
from api.v1.views import app_views
from models.state import State
from models import storage

@app_views.route("/states", methods=['GET'])
@app_views.route("/states/<state_id>", methods=['GET'])
def states(state_id=None):
    if state_id:
        obj = storage.get(State, state_id)
        if obj is not None:
            return obj.to_dict()
        else:
            return page_not_found(404)
    else:
        states = storage.all(State)
        statelist = []
        for state in states.values():
            statelist.append(state.to_dict())
        return jsonify(statelist)

@app_views.route("/states/<state_id>", methods=['DELETE'])
def state_delete(state_id):
    if state_id:
        obj = storage.get(State, state_id)
        if obj is not None:
            storage.delete(obj)
        else:
            return page_not_found(404)
