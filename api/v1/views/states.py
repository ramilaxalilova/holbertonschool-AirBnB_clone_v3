#!/usr/bin/python3
"""
state python
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
def states():
    """documented func"""
    if request.method == "GET":
        states = storage.all(State).values()
        lst = []
        for st in states:
            lst.append(st.to_dict())
        return jsonify(lst)
    elif request.method == "POST":
        data = request.get_json(silent=True)
        if not data:
            abort(400, "Not a JSON")
        elif "name" not in data:
            abort(400, "Missing name")
        new = State(**data)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route(
        "/states/<state_id>",
        methods=["GET", "DELETE", "PUT"],
        strict_slashes=False
        )
def get_states(state_id):
    """documented func"""
    if request.method == "GET":
        st = storage.get(State, state_id)
        if not st:
            abort(404)
        return jsonify(st.to_dict())
    elif request.method == "PUT":
        data = request.get_json(silent=True)
        st = storage.get(State, state_id)
        if not st:
            abort(404)
        elif not data:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(st, key, value)
        storage.save()
        return jsonify(st.to_dict()), 200
    elif request.method == "DELETE":
        st = storage.get(State, state_id)
        if not st:
            abort(404)
        storage.delete(st)
        storage.save()
        return jsonify({}), 200
