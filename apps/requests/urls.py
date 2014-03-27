from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^requests/([0-9]+)/?$', 'apps.requests.views.request_detail'),
    url(r'^requests/status/([A-Za-z]+)/?$', 'apps.requests.views.request_list'),
    url(r'^requests/agency/([A-Za-z ]+)/?$', 'apps.requests.views.agency_list'),
    url(r'^$', 'apps.requests.views.index'),
)
