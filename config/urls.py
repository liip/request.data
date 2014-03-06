from django.conf.urls import patterns, include, url
from config import settings
from apps.requests import urls as request_urls
from apps.pages import urls as page_urls
from apps.emails import urls as email_urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls))
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        url(r'static/(?P<path>.*)$', 'serve', {'document_root': settings.STATIC_ROOT}),
    )

# our apps
urlpatterns += patterns('',
  url(r'^', include(request_urls)),
  url(r'^pages/', include(page_urls)),
  url(r'^emails/', include(email_urls)),)
