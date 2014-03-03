from django.shortcuts import render_to_response, redirect, render
from django.shortcuts import get_object_or_404 as go4
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from apps.requests.models import *
from apps.requests.forms import *
import requests
from django.conf import settings

import json
from django.utils.html import escape
from django.core.context_processors import csrf
from django.utils import formats
from django.core.mail import send_mail, mail_admins
from datetime import datetime


def request_detail(request, request_id):
    return render_to_response("requests/request_detail.html", {"req": go4(Request, id=request_id)})

def create_request(request):
    c = {}
    if request.method == 'POST':
        request_form = RequestForm(request.POST)
        user_form = UserForm(request.POST)
        if request_form.is_valid() and user_form.is_valid:
            new_request = request_form.save(commit=False)
            new_user = user_form.save()
            new_request.creator = new_user
            new_request.save()
            c['req'] = new_request            
            return HttpResponseRedirect('request/' + str(new_request.id), c)
    else:
        c['request_form'] = RequestForm()
        c['user_form'] = UserForm()
        return render(request, 'requests/create.html', c)

def request_list(request, state):
    c = {}
    if state == "all":
        c["state"] = state
        c["requests"] = list(Request.objects.order_by('-created'))
    else:
        c["state"] = state
        c["requests"] = list(Request.objects.order_by('-created').filter(state=state))
    return render_to_response('requests/request_list.html', c)
