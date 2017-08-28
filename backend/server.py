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
from flask import Flask, send_from_directory

from backend.registrar import get_users
from passlib.hash import bcrypt


app = Flask(__name__)

SESSION_KEY = '_cp_username'


@app.route("/<path:path>")
def send(path):
    print(path)
    return send_from_directory("../frontend/", path)


class Server(object):
    def __init__(self):
        self.users = get_users()

    def on_login(self, username):
        """Called on successful login"""
        print(username)

    def on_logout(self, username):
        """Called on logout"""
        print(username)


    @app.route("/login")
    def login(self):
        success = {"operation": "login", "result": "success"}
        error = {"operation": "login", "result": "error"}

        # input_json = cherrypy.request.json
        #
        # if "username" not in input_json or "password" not in input_json:
        #     cherrypy.response.status = 400
        #     return error
        #
        # username = input_json["username"]
        # password = input_json["password"]
        #
        # if self.users.exists(username):
        #     pw_hash = self.users.get_password(username)
        #
        #     if bcrypt.verify(password, pw_hash):
        #         cherrypy.session.regenerate()
        #         cherrypy.session[SESSION_KEY] = username
        #         cherrypy.response.status = 200
        #         return success
        #
        # cherrypy.response.status = 401
        return error

    @app.route("/register")
    def register(self):
        success = {"operation": "registration", "result": "success"}
        error = {"operation": "registration", "result": "error"}

        # input_json = cherrypy.request.json
        #
        # if "username" not in input_json or "password" not in input_json:
        #     print("missing username or password")
        #     cherrypy.response.status = 400
        #     return error
        #
        # username = input_json["username"]
        # password = input_json["password"]
        # pw_hash = bcrypt.encrypt(password)
        #
        # if self.users.register(username, pw_hash):
        #     cherrypy.session.regenerate()
        #     cherrypy.session[SESSION_KEY] = username
        #     cherrypy.response.status = 200
        #     return success
        #
        # cherrypy.response.status = 401
        return error

    @app.route("/logout")
    def logout(self):
        # session = cherrypy.session
        # username = session.get(SESSION_KEY, None)
        # session[SESSION_KEY] = None
        # if username:
        #     self.on_logout(username)
        # raise cherrypy.HTTPRedirect("/")
        return None
