#!/usr/bin/python3
'''handles api routes for State class'''
from api.v1.views import app_views
from models import storage
from datetime import datetime
import flask
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
modelsDict = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
}

@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<id>', methods=['GET'], strict_slashes=False)
def st_get(id=None):
    '''return all states unless id present, then check id and return
    single if present else 404 page
    '''
    if id is None:
        return flask.jsonify([ob.to_dict() for ob in storage.all(
            modelsDict['states']).values()]
        )

    try:
        return flask.jsonify(storage.all()['State.' + id].to_dict())
    except Exception:
        flask.abort(404)


@app_views.route('/states/<id>', methods=['DELETE'], strict_slashes=False)
def st_del(id=None):
    '''delete State by id, return blank json on success else 404 page'''
    if storage.get("State", id):
        storage.get('State', id).delete()
        storage.save()
        return flask.make_response({}, 200)
    else:
        flask.abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def st_post():
    '''create State with input JSON'''
    new_st = flask.request.get_json()
    if not new_st:
        flask.abort(400, 'Not a JSON')
    if 'name' not in new_st.keys():
        flask.abort(400, 'Missing name')
    st = modelsDict['states'](**new_st)
    storage.new(st)
    storage.save()
    return flask.make_response(st.to_dict(), 201)


@app_views.route('/states/<id>', methods=['PUT'], strict_slashes=False)
def st_put(id=None):
    '''update State by id, return updated State else 404 page'''
    try:
        storage.all()['State.' + id].to_dict()
    except Exception:
        flask.abort(404)
    up_st = flask.request.get_json()
    if not up_st:
        flask.abort(400, 'Not a JSON')
    for key in up_st:
        if key not in ['id', 'update_at', 'created_at']:
            setattr(
                storage.all()['State.' + id],
                key,
                up_st[key]
            )
    # may cause checker issue because updated_at wasn't ignored
    setattr(
        storage.all()['State.' + id],
        'updated_at',
        datetime.now()
    )
    storage.save()
    return flask.make_response(storage.all()['State.' + id].to_dict(), 200)
