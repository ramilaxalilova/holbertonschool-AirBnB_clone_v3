#!/usr/bin/python3
"""
amenity python
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route(
        "/amenities",
        methods=["GET", "POST"],
        strict_slashes=False
        )
def am():
    """documented func"""
    if request.method == "GET":
        ams = storage.all(Amenity).values()
        lst = []
        for amn in ams:
            lst.append(amn.to_dict())
        return jsonify(lst)
    elif request.method == "POST":
        data = request.get_json(silent=True)
        if not data:
            abort(400, "Not a JSON")
        elif "name" not in data:
            abort(400, "Missing name")
        new = Amenity(**data)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route(
        "/amenities/<amenity_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False
        )
def get_am(amenity_id):
    """documented func"""
    if request.method == "GET":
        am = storage.get(Amenity, amenity_id)
        if not am:
            abort(404)
        return jsonify(am.to_dict())
    elif request.method == "DELETE":
        am = storage.get(Amenity, amenity_id)
        if not am:
            abort(404)
        storage.delete(am)
        storage.save()
        return jsonify({}), 200
    elif request.method == "PUT":
        data = request.get_json(silent=True)
        am = storage.get(Amenity, amenity_id)
        if not am:
            abort(404)
        elif not data:
            abort(400, "Not a JSON")
        for k, v in data.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(am, k, v)
        storage.save()
        return jsonify(am.to_dict()), 200
