from django.shortcuts import render_to_response, redirect
from django.shortcuts import get_object_or_404 as go4
from django.shortcuts import get_list_or_404 as glo4
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from apps.requests.models import *
from apps.requests.forms import *

import json
from django.conf import settings
from django.utils.html import escape
from django.core.context_processors import csrf
import requests
from django.utils import formats
from django.core.mail import send_mail, mail_admins
from datetime import datetime


def request_detail(request, request_id):
    return render_to_response("requests/request_detail.html", {"req": go4(Request, id=request_id)})

def create_request(request):
    c = {}
    if request.method == 'POST':
        form = RequestForm(request.POST)
        new_request = form.save(commit=False)
    else:
        form = RequestForm()
        c['form'] = form
    return render_to_response("requests/create.html", c)

def request_list(request, state):
    c = {}
    if state == "all":
        c["state"] = state
        c["requests"] = list(Request.objects.order_by('-created'))
    else:
        c["state"] = state
        c["requests"] = list(Request.objects.order_by('-created').filter(state=state))
    return render_to_response("requests/request_list.html", c)
