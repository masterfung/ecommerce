from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns('cart.views',
    url(r'^$', 'view', name='cart'),
    url(r'^add$', 'add_to_cart'),
    url(r'^add_ajax', 'add_ajax', name='add_ajax')

)