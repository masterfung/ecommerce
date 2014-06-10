# Create your views here.
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect, RequestContext, Http404


from products.models import Product
from .models import Cart, CartItem
from .forms import ProductQtyForm

def add_to_cart(request):
    request.session.set_expiry(0)
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
            new_cart, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if new_cart.quantity > 0:
                new_cart.quantity = product_quantity
                new_cart.total = int(new_cart.quantity) * new_cart.product.price
                new_cart.save()
            else:
                pass
            if created:
                print 'Created!'
            print new_cart.product, new_cart.quantity, new_cart.cart
            
            
            
            return HttpResponseRedirect('/cart/')
        return HttpResponseRedirect('/contact/')
    else:
        raise Http404

def view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
    except:
        cart = False

    if cart == False or cart.active == False:
        message = 'Your cart is empty!'
        
    if cart and cart.active:
        cart = cart
        cart.total = 0
        for item in cart.cartitem_set.all():
            cart.total += item.total
            cart.save()
        
    request.session['cart_items'] = len(cart.cartitem_set.all())
    return render_to_response('cart/view.html', locals(), context_instance=RequestContext(request))
