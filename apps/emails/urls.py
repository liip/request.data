from django.conf.urls import patterns, include, url
from apps.emails import views


urlpatterns = patterns('',
  url(r'([a-z0-9]+)/?$', 'apps.emails.views.email_create'),)