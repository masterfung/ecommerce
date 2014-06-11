from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns('orders.views',
    url(r'^$', 'view', name='orders'),

)