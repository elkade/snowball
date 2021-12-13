
# Copyright 2020 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
import random
from flask import Flask, request

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)
moves = ["F", "F", "F", "F",'L', 'R']
attacks = ["F",'T', "T"]
_last_state = None

"""
{
  "_links": {
    "self": {
      "href": "https://foo.com"
    }
  },
  "arena": {
    "dims": [4,3],
    "state": {
      "https://foo.com": {
        "x": 0,
        "y": 0,
        "direction": "N",
        "wasHit": false,
        "score": 0
      }
    }
  }
}
"""
_last_move = "F"

def get_move(dims, state, last_move, last_state):
    if state["x"] == last_state["x"] and state["y"] == last_state["y"]:
        if (state["x"] == 0 and state["direction"] == "W") or (state["x"] == dims[0] - 1 and state["direction"] == "E") or (state["y"] == 0 and state["direction"] == "N") or (state["y"] == dims[1] and state["direction"] == "S"):
            logger.info("Boundary")
            return "R"
        logger.info("Enemy")
        if state["wasHit"]:
            logger.info("wasHit")
            return "L"
        logger.info("Attack")
        return attacks[random.randrange(len(attacks))]
    return None

@app.route("/", methods=['GET'])
def index():
    return "Let the battle begin!"

@app.route("/", methods=['POST'])
def move():
    global _last_state
    global _last_move
    request.get_data()
    logger.info(request.json)
    dims = request.json["arena"]["dims"]
    state = list(request.json["arena"]["state"].values())[0]
    if _last_state is not None:
        move = get_move(dims, state, _last_move, _last_state)
    else:
        move = "F"
    if move is None:
        move = moves[random.randrange(len(moves))]
    _last_move = move
    _last_state = state
    return _last_move

if __name__ == "__main__":
  app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
  
