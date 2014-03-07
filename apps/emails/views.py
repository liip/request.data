import json
import re
import logging
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.utils.html import escape
from django.utils import formats
from django.core.mail import send_mail, mail_admins
from datetime import datetime

from apps.requests.models import User, Request, Comment


@csrf_exempt
def email_create(request, api_key):
    # Get an instance of a logger
    logger = logging.getLogger('email_create')

    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            events = json.loads(json_data['mandrill_events'])
            logger.info('Got POST from Mandrill')

            for event in events:
                sender_email = event['msg']['from_email']
                to_emails = event['msg']['to']
                logger.info('parsing email from ' + sender_email)

                # find the request entry to extract the request-id from
                request_id = None
                for email in to_emails:
                    re_str = r'request\+([0-9]+)\@opendata\.ch'
                    if re.search(re_str, email[0]):
                        request_id = re.search(re_str, email[0]).group(1)
                        break

                logger.info('parsing email from ' + sender_email + ' for request ' + request_id)

                user = User.objects.get(email=sender_email)

                # check if sender is not on blacklist
                if user.blocked == False:
                    logger.info('User ' + sender_email + ' is genuine, parsing email now')
                    
                    # get all the pieces of request/comments in order
                    descriptions = []
                    request = Request.objects.get(pk=request_id)
                    descriptions.extend([request.description])

                    for comment in request.comments.all():
                        descriptions.extend([comment.description])

                    # split the email based on previously entered comments
                    # go through whole email and split it with already entered comments
                    # if the latest comment split the email then the first part must be the new comment
                    # in case the latest comment is not able to split, try with the second latest, etc.
                    for description in reversed(descriptions):
                        desc_split = event['msg']['text'].split(description, 1)
                        if (len(desc_split) == 2) and (len(desc_split[0]) > 0):
                            c = Comment(
                                description=desc_split[0],
                                creator=user,
                                request=request)
                            c.save()
                            break
                else:
                    logger.info('User ' + sender_email + ' is blacklisted, stop processing further')

            return HttpResponse('thanks')

        except:
            return HttpResponse(json.dumps({'message': 'invalid json'}))
    else:
        return HttpResponse(api_key)
