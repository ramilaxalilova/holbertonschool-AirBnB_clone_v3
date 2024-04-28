#!/usr/bin/python3
"""
users python
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route(
        "/users",
        methods=["GET", "POST"],
        strict_slashes=False
        )
def user():
    """documented func"""
    if request.method == "GET":
        users = storage.all(User).values()
        lst = []
        for u in users:
            lst.append(u.to_dict())
        return jsonify(lst)
    elif request.method == "POST":
        data = request.get_json(silent=True)
        if not data:
            abort(400, "Not a JSON")
        elif "email" not in data:
            abort(400, "Missing email")
        elif "password" not in data:
            abort(400, "Missing password")
        new = User(**data)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route(
        "/users/<user_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False
        )
def get_user(user_id):
    """documented func"""
    if request.method == "GET":
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        return jsonify(user.to_dict())
    elif request.method == "DELETE":
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        storage.delete(user)
        storage.save()
        return ({}), 200
    elif request.method == "PUT":
        data = request.get_json(silent=True)
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        elif not data:
            abort(400, "Not a JSON")
        for k, v in data.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(user, k, v)
        storage.save()
        return jsonify(user.to_dict()), 200
