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
import json
from http.server import BaseHTTPRequestHandler

import jsonschema as jsonschema


class IRefuseHTTPRESTEndPoint(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_type = self.headers['Content-Type']

        if post_type == "application/json":
            post_data = self.rfile.read(length).decode("utf-8")

            # You now have a dictionary of the post data, append client's
            # address
            json_data = json.loads(post_data)

            if is_valid_json(json_data):
                json_data["client_ip"] = self.client_address[0]
                json_data["client_port"] = self.client_address[1]
                self.wfile.write("received valid json {}".format(json_data)
                                 .encode("utf-8"))
            else:
                self.wfile.write("received invalid json".encode("utf-8"))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("Invalid request".encode("utf-8"))


schema_start_game = """{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "id": "/",
  "type": "object",
  "properties": {
    "action": {
      "id": "action",
      "type": "string",
      "enum": [
        "START"
      ]
    },
    "players": {
      "id": "players",
      "type": "integer",
      "enum": [
        null,
        3,
        4,
        5
      ]
    }
  },
  "additionalProperties": false,
  "required": [
    "action",
    "players"
  ]
}"""
schema_join_game = """{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "id": "/",
  "type": "object",
  "properties": {
    "action": {
      "id": "action",
      "type": "string",
      "enum": [
        "JOIN"
      ]
    }
  },
  "additionalProperties": false,
  "required": [
    "action"
  ]
}"""
schema_turn_schema = """{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "id": "/",
  "type": "object",
  "properties": {
    "action": {
      "id": "action",
      "type": "string",
      "enum": [
        "PASS",
        "TAKE",
        "QUIT"
      ]
    }
  },
  "additionalProperties": false,
  "required": [
    "action"
  ]
}"""


def is_valid_json(request):
    json_start_schema = json.loads(schema_start_game)
    json_join_schema = json.loads(schema_join_game)
    json_turn_schema = json.loads(schema_turn_schema)
    try:
        jsonschema.validate(request, json_start_schema)
    except:
        try:
            jsonschema.validate(request, json_join_schema)
        except:
            try:
                jsonschema.validate(request, json_turn_schema)
            except:
                return False
    return True