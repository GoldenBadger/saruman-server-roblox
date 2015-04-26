# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os
import time

from django.shortcuts import render
from django.http import JsonResponse
import rpyc
import chess

from .models import Game
from api.chess_engine_pool import Move

rpyc.core.protocol.DEFAULT_CONFIG["allow_pickle"] = True
rpyc.core.protocol.DEFAULT_CONFIG["allow_public_attrs"] = True

def version(request):
    if request.method == "GET":
        config = json.load(open(os.getcwd() + "/config.json"))
        return JsonResponse(config["version"])

def init(request):
    if request.method == "GET":
        elo = int(request.GET.get("elo", -1))
        if elo < 0:
            return JsonResponse({"status": "error",
                "error_desc": "Elo missing or invalid in request."})
        game = Game(player_elo=elo)
        game.save()
        return JsonResponse({"status": "ok", "id": game.id})

def move(request):
    if request.method == "GET":
        game_id = int(request.GET.get("id", -1))
        if game_id < 0:
            return JsonResponse({"status": "error",
                "error_desc": "ID missing or invalid in request."})
                
        position = str(request.GET.get("position", ""))
        if position == "":
            return JsonResponse({"status": "error",
                "error_desc": "Position missing in request."})
        try:
            chess.Board(fen=position)
        except ValueError:
            return JsonResponse({"status": "error",
                "error_desc": "Invalid position in request."})
                
        depth = int(request.GET.get("depth", 7))
        if depth > 7:
            depth = 7
        
        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return JsonResponse({"status": "error",
                "error_desc": "A game with that ID does not exist."})
        move = Move(game_id, position, depth)
        
        with rpyc.connect("localhost", 8001,
            config=rpyc.core.protocol.DEFAULT_CONFIG) as conn:
            conn.root.add_task(move)
            while not conn.root.is_task_complete(game_id):
                time.sleep(1)
            completed_move = conn.root.get_task(game_id)
            return JsonResponse({"status": "ok", "bestmove": completed_move.result})
