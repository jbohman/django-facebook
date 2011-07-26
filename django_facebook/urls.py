from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url('^login/$', 'django_facebook.views.facebook_login', name='facebook_login')
)
