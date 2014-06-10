from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns('cart.views',
    url(r'^add$', 'add_to_cart'),
    url(r'^view$', 'view', name='view_cart'),
)
