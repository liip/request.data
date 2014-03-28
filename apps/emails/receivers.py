import json
import re

from django.utils.log import getLogger
from djrill.signals import webhook_event
from apps.emails.signals import notify_event
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from apps.requests.models import User, Request, Comment
logger = getLogger('emails')

@receiver(webhook_event)
def handle_bounce(sender, event_type, data, **kwargs):
    if event_type == 'hard_bounce' or event_type == 'soft_bounce':
        print "Message to %s bounced: %s" % (
            data['msg']['email'],
            data['msg']['bounce_description']
        )

@receiver(webhook_event)
def handle_inbound(sender, event_type, data, **kwargs):
    if event_type == 'inbound':
        sender_email = data['msg']['from_email']
        to_emails = data['msg']['to']

        # find the request entry to extract the request-id from
        request_id = None
        for email in to_emails:
            re_str = r'request\+([0-9]+)\@opendata\.ch'
            if re.search(re_str, email[0]):
                request_id = re.search(re_str, email[0]).group(1)
                break

        logger.info('Parsing email from ' + sender_email + ' for request ' + request_id)

        try:
            user = User.objects.get(email=sender_email)
        except:
            logger.warn(sender_email + ' tried to email in, but has no account.')
            return

        # check if sender is not on blacklist
        if user.blocked == False:
            logger.info('User ' + sender_email + ' is genuine, parsing email now')
            
            # get all the pieces of request/comments in order
            descriptions = []
            request = Request.objects.get(pk=request_id)
            descriptions.extend([request.description])

            for comment in request.comments.all():
                descriptions.extend([comment.description])

            logger.debug('Got ' + str(len(descriptions)) + ' descriptions for that request')
            email_text = data['msg']['text']

            # run a findall regex against the previous email
            matches = re.findall(r'(^>.+)', email_text, re.MULTILINE)
            if matches and len(matches) >= 1:
                lines = email_text.split('\n')
                for idx, line in enumerate(lines):
                    if line == matches[0]:
                        idx_to_use = idx - 1
                        if lines[idx - 1] == '':
                            idx_to_use = idx - 2

                        comment = ''
                        for line in lines[0:idx_to_use]:
                            comment += line

                        # check if the comment is already in the database
                        # TODO

                        c = Comment(
                            description = comment,
                            creator = user,
                            request = request)
                        logger.info('Saving a comment from ' + sender_email + ' to the database')
                        c.save()
                        notify_event.send(sender=sender, request=request, comment=c, creator=user)
            else:
                logger.info('E-Mail by user ' + sender_email + ' is not matchable.')
                logger.info('E-Mail: ' + email_text)
        else:
            logger.info('User ' + sender_email + ' is blacklisted, stop processing further')

@receiver(notify_event)
def handle_sending_notifications(sender, request, comment, creator, **kwargs):
    # Retrieve all the email addresses this comment needs to be sent to.
    email_addresses = set()
    email_addresses.add(request.creator.email)
    for comment in request.comments.all():
        email_addresses.add(comment.creator.email)
    email_addresses.add(request.agency.email)

    # Remove the email address of the person writing that comment
    # If it's a notification on a request don't do that.
    if comment != None:
        email_addresses.discard(creator.email)

    # Send the notifications to the people involved
    if comment == None:
        subject = '[request.opendata.ch] Request: ' + request.title
        body = request.description
    else:
        subject = '[request.opendata.ch] Comment: ' + request.title
        body = comment.description

    for address in email_addresses:
        msg = EmailMultiAlternatives(
            subject = subject,
            body = body,
            from_email = 'request.opendata.ch <do-not-reply@opendata.ch>',
            to = [address],
            headers = {'Reply-To': 'request+' + str(request.id) + '@opendata.ch'})
        msg.send()

    if comment == None:
        logger.info('Sent all notifications for request: ' + str(request.id))
    else:
        logger.info('Sent all notifications for comment: ' + str(comment.id))
