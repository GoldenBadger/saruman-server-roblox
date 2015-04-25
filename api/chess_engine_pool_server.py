# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# A RPyC server which wraps ChessEnginePool

import json
import multiprocessing

import rpyc

import chess_engine_pool

class ChessEnginePoolService(rpyc.Service):
    
    def __init__(self):
        config = json.load(open(os.getcwd() + "/config.json"))
        self.engine_pool = chess_engine_pool.ChessEnginePool(config["engine_filename",
            multiprocessing.cpu_count() * 2 + 1)
    
    def on_connect(self):
        pass
    
    def on_disconnect(self):
        pass
