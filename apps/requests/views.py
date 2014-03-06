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

def home(request):
    c = {}
    c['request_form'] = RequestForm()
    c['agency_form'] = AgencyForm()
    c['user_form'] = UserForm()
    
    if request.method == 'POST':
        request_form = RequestForm(request.POST)
        agency_form = AgencyForm(request.POST)
        user_form = UserForm(request.POST)

        if request_form.is_valid() and agency_form.is_valid() and user_form.is_valid():
            new_request = request_form.save(commit=False)
            try:
                new_request.creator = User.objects.get(email=user_form.cleaned_data['email'])
            except User.DoesNotExist:
                new_request.creator = user_form.save()
            new_request = request_form.save(commit=False)
            if not new_request.agency:
                new_agency = agency_form.save(commit=False)
                new_agency.email = "unknown@unknown.com"
                new_agency.save()
                agency_form.save_m2m()
                new_request.agency = new_agency
            new_request.save()
            request_form.save_m2m()
            c['req'] = new_request
            return HttpResponseRedirect('requests/' + str(new_request.id), c)
        else:
            return HttpResponseRedirect('/', c)
    else:
        return render(request, "requests/home.html", c)

def request_detail(request, request_id):
    return render(request, "requests/request_detail.html", {"req": go4(Request, id=request_id)})

def request_list(request, state):
    c = {}
    if state == "all":
        c["state"] = state
        c["requests"] = list(Request.objects.order_by('-created'))
    else:
        c["state"] = state
        c["requests"] = list(Request.objects.order_by('-created').filter(state=state))
    return render_to_response('requests/request_list.html', c)
