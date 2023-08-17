#!/usr/bin/env python3
""" flask app for user authentication service """

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def hello_world() -> str:
    """ GET /
    Return:
      - welcome message
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """ POST /users
    Register a user
    Return:
      - message
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = Auth().register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
