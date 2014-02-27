from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^faq/?$', 'apps.pages.views.faq'),
    url(r'^about/?$', 'apps.pages.views.about'),
)
