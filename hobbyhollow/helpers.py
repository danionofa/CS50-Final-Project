import functools
import os
import requests
import urllib.parse
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from hobbyhollow.database import db_session
from hobbyhollow.database import User
from functools import wraps

bp = Blueprint('helpers', __name__, url_prefix='/')

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup(hobby, type):
    """Look up information about movie or show."""
    try:
        api_key = "531c7e2f2bae6e018d58fc7dc016dad7"
        url = f"https://api.themoviedb.org/3/search/{type}?api_key={api_key}&query={hobby}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        info = response.json()
        results = info["results"][0]
        return {
            "image": results["poster_path"],
            "id": int(results["id"]),
            "name": results["name"],
            "genres": results["genre_ids"],
            "overview": results["overview"]
        }
    except (KeyError, TypeError, ValueError, IndexError):
        try:
            info = response.json()
            results = info["results"][0]
            return {
                "image": results["poster_path"],
                "id": int(results["id"]),
                "name": results["title"],
                "genres": str(results["genre_ids"]),
                "overview": results["overview"]
            }
        except(KeyError, TypeError, ValueError, IndexError):
                return None

def suggest(type, genre):
    """Look up a list of movies/shows of a certain type of genre."""
    try:
        api_key = "531c7e2f2bae6e018d58fc7dc016dad7"
        url = f"https://api.themoviedb.org/3/discover/{type}?api_key={api_key}&language=en-US&sort_by=popularity.desc&page=1&with_genres={genre}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None
    
    # If type is show
    try:
        info = response.json()
        results = info["results"]
        list = []
        # Iterate through every result from the response
        for result in results:
            data = {}
            data["image"] = result["poster_path"]
            data["id"] = int(result["id"])
            data["name"] = result["name"]
            data["genres"] = result["genre_ids"]
            data["overview"] = result["overview"]
            list.append(data)
        # Return a list of dictionaries where each result is a dictionary
        return list
    except(KeyError, TypeError, ValueError, IndexError):
        # If type is movie
        try:
            info = response.json()
            results = info["results"]
            list = []
            for result in results:
                data = {}
                data["image"] = result["poster_path"]
                data["id"] = int(result["id"])
                data["name"] = result["title"]
                data["genres"] = result["genre_ids"]
                data["overview"] = result["overview"]
                list.append(data)
            return list
        except(KeyError, TypeError, ValueError, IndexError):
                return None
