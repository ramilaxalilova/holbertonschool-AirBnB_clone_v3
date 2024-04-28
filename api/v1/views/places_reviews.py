#!/usr/bin/python3
"""
reviews python
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route(
        "/places/<place_id>/reviews",
        methods=["GET", "POST"],
        strict_slashes=False
        )
def review_places(place_id):
    """documented func"""
    if request.method == "GET":
        lst = []
        place = storage.get(Place, place_id)

        if place is None:
            abort(404)
        for p in place.reviews:
            lst.append(p.to_dict())

        return jsonify(lst)
    elif request.method == "POST":
        data = request.get_json(silent=True)
        if not data:
            abort(400, "Not a JSON")
        elif "text" not in data:
            abort(400, "Missing text")
        elif "user_id" not in data:
            abort(400, "Missing user_id")

        place = storage.get(Place, place_id)
        if place is None:
            abort(404)

        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)

        new = Review(**data)
        new.place_id = place_id
        new.save()

        return jsonify(new.to_dict()), 201


@app_views.route(
        "/reviews/<review_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False
        )
def revs(review_id):
    """documented func"""
    if request.method == "GET":
        review = storage.get(Review, review_id)

        if review is None:
            abort(404)

        return jsonify(review.to_dict())
    elif request.method == "PUT":
        data = request.get_json(silent=True)
        review = storage.get(Review, review_id)

        if review is None:
            abort(404)
        elif not data:
            abort(400, "Not a JSON")

        for k, v in data.items():
            if k not in ["id",
                         "user_id",
                         "place_id",
                         "created_at",
                         "updated_at"
                         ]:
                setattr(review, k, v)
        storage.save()

        return jsonify(review.to_dict()), 200
    elif request.method == "DELETE":
        review = storage.get(Review, review_id)

        if review is None:
            abort(404)

        storage.delete(review)
        storage.save()

        return jsonify({}), 200
