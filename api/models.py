# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models

# Model to store information about a game (i.e. a series of moves)
class Game(models.Model):
    
    player_elo = models.IntegerField(default=-1)
    exit_reason = models.IntegerField(default=-1)
    plies_moved = models.IntegerField(default=0)
    engine_scores = models.TextField()
