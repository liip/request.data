from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^request/([0-9]+)/?$', 'request_data.request_data.views.data_request'),
    url(r'^$/?$', 'request_data.request_data.views.create_request'),
    url(r'^requests/?$', 'request_data.request_data.views.requests'),
)