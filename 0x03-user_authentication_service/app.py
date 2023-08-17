#!/usr/bin/env python3
""" flask app for user authentication service """

from flask import Flask, jsonify, request, abort, redirect
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


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """ Logs in a user and returns session ID """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    if not Auth().valid_login(email, password):
        abort(401)

    session_id = Auth().create_session(email)

    msg = {"email": email, "message": "logged in"}
    response = jsonify(msg)

    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """ Logs out a user """
    session_id = request.cookies.get('session_id')
    user = Auth().get_user_from_session_id(session_id)

    if user:
        Auth().destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
