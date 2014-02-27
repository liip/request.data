from django.shortcuts import render_to_response, redirect
from django.shortcuts import get_object_or_404 as go4
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
import json
from django.conf import settings
from django.utils.html import escape
from django.core.context_processors import csrf
import requests
from django.utils import formats
from django.core.mail import send_mail, mail_admins
from datetime import datetime

def normalize_path(path):
    if path.endswith('/'):
        path = path[:-1]
    if path != '' and path[0] != '/':
        path = '/' + path
    return path

def data_request(request, request_id):
    c = {}
    req = go4(Request, id=request_id)
    c["request"] = req
    for comment in req.request_comments.all():
        c["comments"].append(comment)
    

def create_request(request, path):
    pass

def requests(request, path):
    pass

def about(request):
    return render_to_response("about.html")

def faq(request):
    return render_to_response("faq.html")
