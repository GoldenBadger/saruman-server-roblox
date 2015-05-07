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
        depth = int(request.GET.get("depth", -1))
        colour = int(request.GET.get("engine_colour", -1))
        if elo < 0:
            return JsonResponse({"status": "error",
                                 "error_desc": "Elo missing or invalid in request."})
        if depth < 0:
            return JsonResponse({"status": "error",
                                 "error_desc": "Depth missing or invalid in request."})
        if colour < 0:
            return JsonResponse({"status": "error",
                                 "error_desc": "Engine colour missing or invalid in request."})
        game = Game(player_elo=elo, engine_colour=colour, game_depth=depth)
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
        if depth > 7 or depth < 1:
            return JsonResponse({"status": "error",
                                 "error_desc": "Depth missing or invalid in request."})
        
        try:
            game = Game.objects.get(id=game_id)
            if game.game_over:
                return JsonResponse({"status": "error",
                    "error_desc": "A game with that ID does not exist."})
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
            game.engine_scores += (str(completed_move.score) + " ")
            game.save()
            return JsonResponse({"status": "ok", "bestmove": completed_move.result})

def quit(request):
    if request.method == "GET":
        game_id = int(request.GET.get("id", -1))
        if game_id < 0:
            return JsonResponse({"status": "error",
                                 "error_desc": "ID missing or invalid in request."})
        
        exit_reason = int(request.GET.get("reason", -1))
        if exit_reason < 0 or exit_reason > 7:
            return JsonResponse({"status": "error",
                                 "error_desc": "Reason missing or invalid in request."})
        
        plies_moved = int(request.GET.get("plies", -1))
        if plies_moved < 0:
            return JsonResponse({"status": "error",
                                 "error_desc": "Number of plies missing or invalid in request."})
        
        try:
            game = Game.objects.get(id=game_id)
            if game.game_over:
                return JsonResponse({"status": "error",
                                     "error_desc": "A game with that ID does not exist."})
        except Game.DoesNotExist:
            return JsonResponse({"status": "error",
                                 "error_desc": "A game with that ID does not exist."})
        
        game.exit_reason = exit_reason
        game.plies_moved = plies_moved
        game.game_over = True
        game.save()
        
        return JsonResponse({"status": "ok"})
