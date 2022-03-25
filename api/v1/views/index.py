#!/usr/bin/python3
"""Pulls up the index of the web application"""
from flask import jsonify, Flask
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """return status of the index if route opens successfully"""
    resp = {"status": "OK"}
    return jsonify(resp)
