from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect, RequestContext

from products.models import Product
from .forms import ProductQtyForm
from .models import Cart, CartItem

def add_to_cart(request):
	try:
		cart_id = request.session('cart_id')
	except Exception: #none exist then new one is made
		cart = Cart()
		cart.save()
		request.session['cart_id'] = cart.id
		cart_id = cart_id

	if request.method == 'POST':
		form = ProductQtyForm(request.POST)
		if form.is_valid():
			product_slug = form.cleaned_data['slug']
			product_quantity = form.cleaned_data['quantity']
			try:
				product = Project.object.get(slug=slug)
			except Exception:
				product = None
			new_cart = CartItem(cart=cart_id, product=product, quantity=product_quantity)
			new_cart.save()

			return HttpResponseRedirect('/products')
	else:
			raise Http404