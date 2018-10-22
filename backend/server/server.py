# -*- encoding: UTF-8 -*-
"""
'I Refuse' web application
Copyright (C) 2017  Jacob Delgado

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from flask import Flask, send_from_directory, request, session, jsonify
import bcrypt

from backend.server.registrar import get_users
app = Flask(__name__)
app.secret_key = 'You Will Never Guess'

SALT = bcrypt.gensalt()
users = get_users()


@app.route("/<path:path>")
def send(path):
    print(path)
    return send_from_directory("../frontend/", path)


@app.route("/login", methods=['POST'])
def login():
    success = {"operation": "login", "result": "success"}
    error = {"operation": "login", "result": "error"}

    if not request.is_json:
        return 'Bad Request', 404

    input_json = request.get_json()

    if "username" not in input_json or "password" not in input_json:
        return jsonify(error), 400

    username = input_json["username"]
    password = input_json["password"]

    if users.exists(username):
        pw_hash = users.get_password(username)

        if bcrypt.hashpw(password.encode("utf8"), pw_hash):
            session['username'] = username
            return jsonify(success), 200

    return jsonify(error), 401


@app.route("/register", methods=['POST'])
def register():
    success = {"operation": "registration", "result": "success"}
    error = {"operation": "registration", "result": "error"}

    if not request.is_json:
        return 'Bad Request', 404

    input_json = request.get_json()

    if "username" not in input_json or "password" not in input_json:
        print("missing username or password")
        return jsonify(error), 400

    username = input_json["username"]
    password = input_json["password"]
    pw_hash = bcrypt.hashpw(password.encode("utf8"), SALT)

    if users.register(username, pw_hash):
        session['username'] = username
        return jsonify(success), 200

    return jsonify(error), 401


@app.route("/logout", methods=['POST'])
def logout():
    if 'username' in session.keys():
        session.pop('username')
    return 'Logged out', 200


if __name__ == "__main__":
    users.initialize()
    app.run()
