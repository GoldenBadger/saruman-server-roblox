import json
import os

from django.shortcuts import render
from django.http import JsonResponse


def version(request):
    if request.method == "GET":
        config = json.load(open(os.getcwd() + "/config.json"))
        return JsonResponse(config["version"])
