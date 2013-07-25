from django.conf.urls.defaults import *
from django.contrib import admin
from sms.views import IndexView


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), {}, 'home'),
                       
    # include our SMS app
    url(r'^', include('sms.urls')),

    # users patterns ..
    url(r'^users/', include('smartmin.users.urls')),
)
