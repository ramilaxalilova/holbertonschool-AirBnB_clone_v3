#!/usr/bin/python3
"""
cities python
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route(
        "/states/<state_id>/cities",
        methods=["GET", "POST"],
        strict_slashes=False
        )
def get_city(state_id):
    """documented func"""
    if request.method == "GET":
        lst = []
        st = storage.get(State, state_id)

        if st is None:
            abort(404)
        for c in st.cities:
            lst.append(c.to_dict())

        return jsonify(lst)
    elif request.method == "POST":
        data = request.get_json(silent=True)
        st = storage.get(State, state_id)

        if st is None:
            abort(404)
        if not data:
            abort(400, "Not a JSON")
        if "name" not in data:
            abort(400, "Missing name")

        new = State(**data)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route(
        "/cities/<city_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False
        )
def cities_id(city_id):
    """documented func"""
    if request.method == "GET":
        city = storage.get(City, city_id)

        if city is None:
            abort(404)
        return jsonify(city.to_dict())
    elif request.method == "PUT":
        data = request.get_json(silent=True)
        city = storage.get(City, city_id)

        if city is None:
            abort(404)
        elif not data:
            abort(400, "Not a JSON")

        for k, v in data.items():
            if k not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city, k, v)
        storage.save()

        return jsonify(city.to_dict()), 200
    elif request.method == "DELETE":
        city = storage.get(City, city_id)

        if city is None:
            abort(404)

        storage.delete(city)
        storage.save()

        return jsonify({}), 200
