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
import json
import jsonschema as jsonschema

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
