# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# A RPyC server which wraps ChessEnginePool

#!/usr/bin/env python3

import os
import json
import multiprocessing

import rpyc

import chess_engine_pool

rpyc.core.protocol.DEFAULT_CONFIG["allow_pickle"] = True

class ChessEnginePoolService(rpyc.Service):
    
    def on_connect(self):
        print("Connection made.")
    
    def on_disconnect(self):
        print("Connection terminated.")
        
    def exposed_add_task(self, move):
        print("Task added. ID: " + str(move.move_id))
        return engine_pool.add_task(move)
    
    def exposed_is_task_complete(self, move_id):
        return engine_pool.is_task_complete(move_id)
    
    def exposed_get_task(self, move_id):
        print("Returned task. ID: " + str(move_id))
        return engine_pool.get_task(move_id)

if __name__ == "__main__":
    config = json.load(open(os.getcwd() + "/config.json"))
    engine_pool = chess_engine_pool.ChessEnginePool(config["engine_filename"],
        multiprocessing.cpu_count() * 2 + 1)
    
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(ChessEnginePoolService, port=8001,
        protocol_config=rpyc.core.protocol.DEFAULT_CONFIG)
    t.start()
