from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^/?$', 'apps.requests.views.home'),
    url(r'^create/?$', 'apps.requests.views.create_request'),
    url(r'request/([0-9]+)/?$', 'apps.requests.views.request_detail'),
    url(r'^requests/([A-Za-z]+)/?$', 'apps.requests.views.request_list'),
)
