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

            # split the email based on previously entered comments
            # go through whole email and split it with already entered comments
            # if the latest comment split the email then the first part must be the new comment
            # in case the latest comment is not able to split, try with the second latest, etc.
            for description in reversed(descriptions):
                desc_split = data['msg']['text'].split(description, 1)
                if (len(desc_split) == 2) and (len(desc_split[0]) > 0):
                    c = Comment(
                        description=desc_split[0],
                        creator=user,
                        request=request)
                    logger.info('Saving a comment from ' + sender_email + ' to the database')
                    c.save()
                    notify_event.send(sender=sender, request=request, comment=c, creator=user)
                    break

                # if first element is an empty string it means that the comment is already there, possibly because the email has been mistakenly resent.
                elif (len(desc_split) == 2) and (len(desc_split[0]) == 0):
                    logger.info('Comment is already in the system, therefore don\'t add again')
                    break
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
    email_addresses.discard(creator.email)
    logger.info(len(email_addresses))

    # Send the notifications to the people involved
    for address in email_addresses:
        msg = EmailMultiAlternatives(
            subject = '[request.opendata.ch] Comment',
            body = comment.description,
            from_email = 'request.opendata.ch <do-not-reply@opendata.ch>',
            to = [address],
            headers = {'Reply-To': 'request+' + str(request.id) + '@opendata.ch'})
        msg.send()

    logger.info('Sent all notifications for comment: ' + str(comment.id))
