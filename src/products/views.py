from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext, get_object_or_404

from cart.forms import ProductQtyForm
from .models import Product


def all_products(request):
    products = Product.objects.all()
    return render_to_response('products/all.html', locals(), context_instance=RequestContext(request))


def single_product(request, slug):
    add_product = ProductQtyForm()
    product = get_object_or_404(Product, slug=slug)
    return render_to_response('products/single.html', locals(), context_instance=RequestContext(request))

def search(request):
	try:
		q = request.GET.get('q', '')
	except:
		q = False

	if q: #iterable search method
		k = q.split()
		if len(k) >=2:
			products = []
			for i in k:
				all_products = Product.objects.filter(title__icontains=i).distinct()
				for product in all_products:
					if product not in products:
						products.append(product)
		else:
			products = Product.objects.filter(title__icontains=q) #icontains is not case sensitive
	return render_to_response('products/search.html', locals(), context_instance=RequestContext(request))