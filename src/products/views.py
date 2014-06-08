from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext, get_object_or_404

from .models import Product

def all_products(request):
    products = Product.objects.filter(active=True)
    return render_to_response('products/all.html', locals(), context_instance=RequestContext(request))
    
