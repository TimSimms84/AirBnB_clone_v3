#!/usr/bin/python3
"""
Task 12
"""

from models.user import User
from models.review import Review
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Returns all reviwers of a place by ID"""
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review_by_id(review_id):
    """gets a review by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    return jsonify(review.to_dict())


@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """post a review"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    newReview = request.get_json()
    user = storage.get(User, newReview['user_id'])
    if user is None:
        return abort(404)
    if 'text' not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)
    newReview['place_id'] = place_id
    instance = Review(**newReview)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    notThese = ["id", "created_at", "updated_at", "place_id", "user_id"]
    data = request.get_json()
    for key, value in data.items():
        if key not in notThese:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
