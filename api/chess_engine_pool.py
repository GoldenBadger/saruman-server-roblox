# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Implements a thread pool system for processing chess move requests.

import sys
import uuid
from queue import Empty
from subprocess import Popen, PIPE
from multiprocessing import Process, Queue, Manager

# First, we need to define what a move is.
class Move(object):
    
    def __init__(self, game_id, position, depth, result=None):
        self.game_id = game_id
        self.position = position
        self.depth = depth
        self.result = result

# Now we can define the actual pool
class ChessEnginePool(object):
    
    def __init__(self, engine_filename, num_engines):
        self._manager = Manager()
        self._pool_input = Queue()
        self._pool_output = self._manager.dict()
        
        self._engine_cancel = self._manager.Value("b", 0)
        self._engine_processes = []
        for i in range(num_engines):
            engine_process = Process(target=self._engine_worker_work,
                args=(engine_filename, self._engine_cancel))
            engine_process.daemon = True
            engine_process.start()
            self._engine_processes.append(engine_process)
    
    def add_task(self, move):
        self._pool_input.put(move)
    
    def is_task_complete(self, move_id):
        if move_id in self._pool_output:
            return True
        else:
            return False
        
    def get_task(self, move_id):
        try:
            move = self._pool_output[move_id]
            del self._pool_output[move_id]
            return move
        except KeyError as error:
            raise ValueError("Task is not complete yet. Wait until " \
                "is_task_complete returns True") from error
    
    def __del__(self):
        self._engine_cancel.value = 1
        for engine_process in self._engine_processes:
            engine_process.join()
        
    
    def _engine_worker_work(self, engine_filename, engine_cancel):
        engine_process = Popen(engine_filename, stdin=PIPE, stdout=PIPE,
            universal_newlines=True, bufsize=1)
            
        while engine_cancel.value == 0:
            try:
                move = self._pool_input.get(True, 1)
                engine_process.stdin.write("position fen " + move.position + "\n")
                engine_process.stdin.write("go depth " + str(move.depth) + "\n")
                output = engine_process.stdout.readline()
                while not output.startswith("bestmove"):
                    output = engine_process.stdout.readline()
                if len(output) >= 14:
                    move.result = output[9:14]
                elif len(output) == 13:
                    move.result = output[9:13]
                else:
                    sys.stderr.write("(EE) Engine returned invalid move. Output: "
                        + output + "\n")
                self._pool_output[move.game_id] = move
            except Empty:
                pass
                
        engine_process.terminate()
