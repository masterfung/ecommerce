from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns('products.views',
    url(r'$', 'all_products', name='products'),
)
