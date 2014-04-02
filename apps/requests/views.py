from django.shortcuts import render_to_response, redirect, render
from django.shortcuts import get_object_or_404 as go4
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from apps.requests.models import *
from apps.requests.forms import *
import requests
from django.conf import settings

from django.utils.log import getLogger
logger = getLogger('requests')

import json
from django.utils.html import escape
from django.core.context_processors import csrf
from django.utils import formats
from django.core.mail import send_mail, mail_admins
from datetime import datetime

from apps.emails.signals import notify_event

def index(request):
    c = {}
    c['request_form'] = RequestForm()
    # c['agency_form'] = AgencyForm()
    c['user_form'] = UserForm()
    c['requests'] = list(Request.objects.order_by('-created'))

    if request.method == 'POST':
        logger.debug('Got a POST request to create a new data request')
        request_form = RequestForm(request.POST)
        # agency_form = AgencyForm(request.POST)
        user_form = UserForm(request.POST)

        logger.debug('request_form is valid: ' + str(request_form.is_valid()))
        # logger.debug('agency_form is valid: ' + str(agency_form.is_valid()))
        logger.debug('user_form is valid: ' + str(user_form.is_valid()))

        if request_form.is_valid():
            logger.debug('The request data is valid')

            # Linking the creator to the request
            new_request = request_form.save(commit=False)
            if user_form.is_valid():
                try:
                    new_request.creator = User.objects.get(email=user_form.cleaned_data['email'])
                except User.DoesNotExist:
                    new_user = User(name=user_form.cleaned_data['name'], email=user_form.cleaned_data['email'])
                    new_user.save()
                    new_request.creator = new_user
            else:
                return HttpResponseRedirect('/', c)

            # Linking the agency to the request
            # new_request = request_form.save(commit=False)
            # if not new_request.agency:
                # new_agency = agency_form.save(commit=False)
                # new_agency.email = "unknown@unknown.com"
                # new_agency.save()
                # agency_form.save_m2m()
                # new_request.agency = new_agency

            # Fully saving the request into the database
            new_request.save()
            request_form.save_m2m()
            logger.debug('Request: ' + str(new_request.id) + ' saved')

            # Add the creator as a user of the request
            new_request.users.add(new_request.creator)
            logger.debug([user.name for user in new_request.users.all()])

            # Notify the agency and the user that the request has been received.
            notify_event.send(sender=request, request=new_request, comment=None, creator=new_request.creator)

            c['req'] = new_request
            return HttpResponseRedirect('requests/' + str(new_request.id), c)
        else:
            return HttpResponseRedirect('/', c)
    else:
        return render(request, "requests/index.html", c)

def request_detail(request, request_id):
    c = {}
    req = go4(Request, id=request_id)
    c['comment_form'] = CommentForm()
    c['user_form'] = UserForm()
    c['req'] = req

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        user_form = UserForm(request.POST)

        if comment_form.is_valid() and user_form.is_valid():
            # Save the description to a new comment
            new_comment = comment_form.save(commit=False)

            # Set the comment's creator to the user, and add user if it doesn't exist
            try:
                new_comment.creator = User.objects.get(email=user_form.cleaned_data['email'])
            except User.DoesNotExist:
                new_user = User(name=user_form.cleaned_data['name'], email=user_form.cleaned_data['email'])
                new_user.save()
                new_comment.creator = new_user

            # Set the comment's request
            new_comment.request = req

            # Add the commenter to the users of the request
            req.users.add(new_comment.creator)

            #Save the comment
            new_comment.save()
            comment_form.save_m2m()

            # Notify the agency and the users subscribed about the new comments
            notify_event.send(
                sender=request,
                request=new_comment.request,
                comment=new_comment,
                creator=new_comment.creator)

    return render(request, "requests/request_detail.html", c)

def request_list(request, state):
    c = {}
    if state == "all":
        c["state"] = state
        c["requests"] = list(Request.objects.order_by('-created'))
    else:
        c["state"] = state
        c["requests"] = list(Request.objects.order_by('-created').filter(state=state))
    return render_to_response('requests/request_list.html', c)

def agency_list(request, agency_name):
    c = {}
    agency = go4(Agency, a_name=agency_name)
    c["agency"] = agency
    c["requests"] = list(Request.objects.order_by('-created').filter(agency=agency))
    return render_to_response('requests/agency_list.html', c)
