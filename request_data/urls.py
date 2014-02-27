from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^request/([0-9]+/?$', 'request_data.request_data.views.request'),
    url(r'^$/?$', 'request_data.request_data.views.create_request'),
    url(r'^faq/?$', 'request_data.request_data.views.faq'),
    url(r'^about/?$', 'request_data.request_data.views.about')
)
