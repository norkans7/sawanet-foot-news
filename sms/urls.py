from django.conf.urls.defaults import *
from .views import *

urlpatterns = patterns('',
     (r'^sms/receive$', receive))

urlpatterns += SMSCRUDL().as_urlpatterns()
urlpatterns += TagCRUDL().as_urlpatterns()
