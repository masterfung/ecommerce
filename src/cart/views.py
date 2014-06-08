# Create your views here.
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect, RequestContext, Http404


from products.models import Product
from .models import Cart, CartItem
from .forms import ProductQtyForm

def add_to_cart(request):
    try:
        cart_id = request.session['cart_id']
    except:
        cart = Cart()
        cart.save()
        request.session['cart_id'] = cart.id
        cart_id = cart.id

    if request.method == "POST":
        form = ProductQtyForm(request.POST)
        if form.is_valid():
            product_slug = form.cleaned_data['slug']
            product_quantity = form.cleaned_data['quantity']
            try:
                product = Product.objects.get(slug=product_slug)
            except Exception:
                product = None
            try:
                cart = Cart.objects.get(id=cart_id)
            except Exception:
                cart = None
            new_cart = CartItem(cart=cart, product=product, quantity=product_quantity)
            new_cart.save()
            print new_cart.product, new_cart.quantity, new_cart.cart
            return HttpResponseRedirect('/products/')
        return HttpResponseRedirect('/contact/')
    else:
        raise Http404
