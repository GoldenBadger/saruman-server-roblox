# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
from subprocess import Popen

from django.apps import AppConfig

class SarumanServerAPIConfig(AppConfig):
    
    name = "api"
    verbose_name = "Saruman Server API"
    
    def ready(self):
        Popen(os.getcwd() + "/api/chess_engine_pool_server.py")
