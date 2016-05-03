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
import abc
import sqlite3


def getUsers(debug=False):
    if debug:
        return UsersMock()
    return UsersTable()


class Users(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def initialize(self):
        """Initializes the data store"""

    @abc.abstractmethod
    def exists(self, username):
        """Returns a boolean if user is known"""

    @abc.abstractmethod
    def register(self, username, password):
        """Registers the user and their password in the data store"""

    @abc.abstractmethod
    def get_password(self, username):
        """Returns the password as it is stored for the given user"""

    @abc.abstractmethod
    def destroy(self):
        """Destroys artifacts of all users"""


class UsersTable(Users):
    DB_STRING = "users.db"

    def initialize(self):
        with sqlite3.connect(self.DB_STRING) as con:
            con.execute("CREATE TABLE users (username text, password varchar(60))")

    def exists(self, username):
        with sqlite3.connect(self.DB_STRING) as con:
            cmd = "SELECT COUNT(*) AS c FROM users WHERE username=? LIMIT 1"
            return con.execute(cmd, (username,)).fetchone() == (1,)

    def register(self, username, password):
        with sqlite3.connect(self.DB_STRING) as con:
            if self.exists(username):
                return False

            cmd = "INSERT INTO users VALUES (?, ?)"
            print(username, password)
            con.execute(cmd, (username, password))
            con.commit()
            return True

    def get_password(self, username):
        with sqlite3.connect(self.DB_STRING) as con:
            cmd = "SELECT * FROM users WHERE username=? LIMIT 1"
            return con.execute(cmd, (username,)).fetchone()[1]

    def destroy(self):
        with sqlite3.connect(self.DB_STRING) as con:
            con.execute("DROP TABLE users")


class UsersMock(Users):
    def __init__(self):
        self.users = {}

    def initialize(self):
        pass

    def exists(self, username):
        return username in self.users

    def register(self, username, password):
        if self.exists(username):
            return False
        self.users[username] = password
        return True

    def get_password(self, username):
        return self.users[username]

    def destroy(self):
        self.users = {}
