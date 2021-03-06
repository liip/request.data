from django.conf.urls import patterns, include, url
from config import settings
from apps.requests import urls as request_urls
from apps.pages import urls as page_urls

import apps.emails.receivers
from djrill import urls as djrill_urls

from django.contrib import admin

# To see some Mandrill stats in the Admin Interface
from djrill import DjrillAdminSite
admin.site = DjrillAdminSite()

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
  url(r'^emails/', include(djrill_urls)),
  )
