#!/usr/bin/env python3
"""new view for Session Authentication"""

from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """POST /api/v1/auth_session/login
    Return:
      - User object JSON represented
    """
    from flask import request, jsonify
    from models.user import User
    from os import getenv

    email = request.form.get('email')
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(users[0].id)
    cookie_name = getenv('SESSION_NAME')
    response = jsonify(users[0].to_json())
    response.set_cookie(cookie_name, session_id)
    return response
