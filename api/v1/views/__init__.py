#!/usr/bin/python3
'''views initialization'''
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

from flask import Blueprint

modelsDict = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
}

app_views = Blueprint("/api/v1", __name__, url_prefix="/api/v1")
from api.v1.views.index import *  # keep below app_views to resolve circular
import api.v1.views.states
