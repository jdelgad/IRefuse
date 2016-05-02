"""
Copyright (c) 2016 Jacob Delgado,
This file is part of I Refuse.

'I Refuse' is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import cherrypy
from backend.auth import require

SESSION_KEY = '_cp_username'


class Server(object):
    def on_login(self, username):
        """Called on successful login"""
        print(username)

    def on_logout(self, username):
        """Called on logout"""
        print(username)

    @cherrypy.expose
    def index(self):
        return open('frontend/index.html')

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def login(self):
        success = {"operation": "login", "result": "success"}
        error = {"operation": "login", "result": "error"}

        input_json = cherrypy.request.json

        if "email" not in input_json or "password" not in input_json:
            cherrypy.response.status = 400
            return error

        username = input_json["email"]
        password = input_json["password"]

        if username == "jacob@gmail.com" and password == "password":
            cherrypy.session.regenerate()
            cherrypy.session[SESSION_KEY] = username
            cherrypy.response.status = 200
            return success

        cherrypy.response.status = 400
        return error

    @cherrypy.expose
    @require()
    def game(self):
        return open('frontend/game.html')

    @cherrypy.expose
    @require()
    def logout(self):
        session = cherrypy.session
        username = session.get(SESSION_KEY, None)
        session[SESSION_KEY] = None
        if username:
            self.on_logout(username)
        raise cherrypy.HTTPRedirect("/")
