#!/usr/bin/python
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
from http.server import HTTPServer

from restful.endpoint import IRefuseHTTPRESTEndPoint


def main():
    ip = "127.0.0.1"
    port = 8000
    server_address = (ip, 8000)
    httpd = HTTPServer(server_address, IRefuseHTTPRESTEndPoint)
    print("Running server on {}:{}".format(ip, port))
    httpd.serve_forever()

if __name__ == "__main__":
    main()
