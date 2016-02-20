from django.conf.urls import include, url
from django.contrib import admin
from restServer.views import *

urlpatterns = [

	url(r'^api/request/$',startRequest, name='start'),
	url(r'^api/kill/$',killRequest, name='kill'),
	url(r'^api/active/$',activeRequests, name='active'),
	url(r'^api/serverStatus/$',timeRemaining, name='status'),

]
