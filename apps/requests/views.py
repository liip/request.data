from django.shortcuts import render_to_response, redirect
from django.shortcuts import get_object_or_404 as go4
from django.shortcuts import get_list_or_404 as glo4
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from apps.requests.models import *

import json
from django.conf import settings
from django.utils.html import escape
from django.core.context_processors import csrf
import requests
from django.utils import formats
from django.core.mail import send_mail, mail_admins
from datetime import datetime


def request_detail(request, request_id):
    return render_to_response("request_detail.html", {"req": go4(Request, id=request_id)})

def create_request(request):
    return render_to_response("create.html")

def request_list(request, state):
    c = {}
    if state == "all":
        c["state"] = state
        c["requests"] = glo4(Request)
    else:
        c["state"] = state
        c["requests"] = glo4(Request, state=state)
    return render_to_response("request_list.html", c)
