#!/usr/bin/python3
"""doc"""


from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    states = storage.count('State')
    amenities = storage.count('Amenity')
    cities = storage.count('City')
    places = storage.count('Place')
    reviews = storage.count('Review')
    users = storage.count('User')
    return {
        "amenities": amenities,
        "cities": cities,
        "places": places,
        "reviews": reviews,
        "states": states,
        "users": users
    }
