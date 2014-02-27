from django.shortcuts import render_to_response, redirect
from django.shortcuts import get_object_or_404 as go4
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
import json
from django.conf import settings
from django.utils.html import escape
from django.core.context_processors import csrf
from django.utils import formats
from django.core.mail import send_mail, mail_admins
from datetime import datetime

def about(request):
    return render_to_response('pages/about.html')

def faq(request):
    return render_to_response("pages/faq.html")
