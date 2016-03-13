#!/usr/bin/python
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import jsonschema as jsonschema


class IRefuseHTTPRESTEndPoint(BaseHTTPRequestHandler):

    def do_POST(self):
        print(self.headers)
        length = int(self.headers['Content-Length'])
        post_type = self.headers['Content-Type']

        if post_type == "application/json":
            post_data = self.rfile.read(length).decode("utf-8")

            # You now have a dictionary of the post data
            json_data = json.loads(post_data)

            if is_valid_json(json_data):
                self.wfile.write("received valid json {}".format(post_data)
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


def main():
    ip = "127.0.0.1"
    port = 8000
    server_address = (ip, 8000)
    httpd = HTTPServer(server_address, IRefuseHTTPRESTEndPoint)
    print("Running server on {}:{}".format(ip, port))
    httpd.serve_forever()

if __name__ == "__main__":
    main()
