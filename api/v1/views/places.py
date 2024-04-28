#!/usr/bin/python3
"""
places python
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route(
        "/cities/<city_id>/places",
        methods=["GET", "POST"],
        strict_slashes=False
        )
def places_id(city_id):
    """documented func"""
    if request.method == "GET":
        lst = []
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        for c in city.places:
            lst.append(c.to_dict())

        return jsonify(lst)
    elif request.method == "POST":
        data = request.get_json(silent=True)
        city = storage.get(City, city_id)

        if not data:
            abort(400, "Not a JSON")
        elif city is None:
            abort(404)
        elif "name" not in data:
            abort(400, "Missing name")
        elif "user_id" not in data:
            abort(400, "Missing user_id")

        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)

        data['city_id'] = city_id
        new = Place(**data)
        new.save()

        return jsonify(new.to_dict()), 201


@app_views.route(
        "/places/<place_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False
        )
def get_places(place_id):
    """documented func"""
    if request.method == "GET":
        place = storage.get(Place, place_id)

        if place is None:
            abort(404)

        return jsonify(place.to_dict())
    elif request.method == "PUT":
        data = request.get_json(silent=True)
        place = storage.get(Place, place_id)

        if not data:
            abort(400, "Not a JSON")
        elif place is None:
            abort(404)

        for k, v in data.items():
            if k not in ["id",
                         "user_id",
                         "city_id",
                         "created_at",
                         "updated_at"
                         ]:
                setattr(place, k, v)
        storage.save()

        return jsonify(place.to_dict()), 200
    elif request.method == "DELETE":
        place = storage.get(Place, place_id)

        if place is None:
            abort(404)

        storage.delete(place)
        storage.save()

        return jsonify({}), 200
