# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os

from django.shortcuts import render
from django.http import JsonResponse


def version(request):
    if request.method == "GET":
        config = json.load(open(os.getcwd() + "/config.json"))
        return JsonResponse(config["version"])
