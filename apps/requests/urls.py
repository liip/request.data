from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^requests/([0-9]+)/?$', 'apps.requests.views.request_detail'),
    url(r'^requests/([A-Za-z]+)/?$', 'apps.requests.views.request_list'),
    url(r'^$', 'apps.requests.views.index'),
)
