from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'request/([0-9]+)/?$', 'apps.requests.views.data_request'),
    url(r'^/?$', 'apps.requests.views.create_request'),
    url(r'^requests/?$', 'apps.requests.views.requests'),
)
