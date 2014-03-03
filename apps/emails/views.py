import json
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.utils.html import escape
from django.utils import formats
from django.core.mail import send_mail, mail_admins
from datetime import datetime

from apps.requests.models import *


@csrf_exempt
def email_create(request, api_key):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            events = json.loads(json_data['mandrill_events'])
            return HttpResponse(len(events))

        except:
            return HttpResponse(json.dumps({'message': 'invalid json'}))

        # return HttpResponse(request.body)
        # print 'Hello'
        # return HttpResponse('Hello')
        # json_data = simplejson.loads(request.body)
        # print json_data
        # return HttpResponse(simplejson.dumps(json_data))
    else:
        # print 'non post request'
        return HttpResponse(api_key)
        # return Http404
