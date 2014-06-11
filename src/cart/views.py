# Create your views here.
import datetime

from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect, RequestContext, Http404
from django.contrib.auth.decorators import login_required

from orders.models import Order, ShippingStatus
from orders.custom import id_generator

from profiles.forms import AddressForm
from profiles.models import Profile
from products.models import Product


from .models import Cart, CartItem
from .forms import ProductQtyForm



import stripe
stripe.api_key='sk_test_UZ7gkbevnGjtz2nu3olxTHtU'

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
            #Below updates quantity
            if product_quantity > 0:
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


def add_stripe(user):
    profile, created = Profile.objects.get_or_create(user=user)
    if len(profile.stripe_id) > 1:
        print 'exsits'
        pass
    else:
        new_customer = stripe.Customer.create(
            email = user.email,
            description = "Added to stripe on %s" %(datetime.datetime.now())
        )
        profile.stripe_id = new_customer.id
        profile.save()
    
    return profile.stripe_id




def view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['cart_items'] = len(cart.cartitem_set.all())
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
    
    try:
        stripe_id = add_stripe(request.user)
    except:
        pass

    return render_to_response('cart/view.html', locals(), context_instance=RequestContext(request))



@login_required
def checkout(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
    except:
        cart = False
        return HttpResponseRedirect('/cart')
    
    amount = int(cart.total * 100)
    
    try:
        stripe_id = add_stripe(request.user)
    except:
        pass

    new_number = id_generator()
        
    new_order, created = Order.objects.get_or_create(cart=cart, user=request.user)
    
    if created:
        new_order.order_id = str(new_number[:2]) + str(new_order.cart.id) + str(new_number[3:])
        new_order.status = 'Started'
        new_order.save()

    address_form = AddressForm(request.POST or None)
    if request.method == "POST":
        address_form = AddressForm(request.POST)
        token = request.POST['stripeToken']
        profile = request.user.get_profile()
        customer = stripe.Customer.retrieve(stripe_id)
        new_card = customer.cards.create (card=token)

        if address_form.is_valid():
            form = address_form.save(commit=False)
            print form
            if address_form.cleaned_data['save_card'] == True:
                #save card info
                new_card.address_line1 = form.address1
                if len(form.address2) > 1:
                    new_card.address_line2 = form.address2
                new_card.address_city = form.city
                new_card.address_zip = form.postal_code
                new_card.address_country = form.country
                new_card.save()
                try:
                    form.user = request.user
                    form.save()
                    print 'form saved'
                except:
                    pass
            else:
                print 'did not save your card'

            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                customer= customer.id,
                description = "Payment for order %s" %(new_order.order_id)
            )
            if charge:
                print 'charged'
                new_order.status = 'Collected' #changes the status in the admin panel! :)
                new_order.cc_four = new_card.last4
                new_order.address = form
                new_order.save()
                add_shipping = ShippingStatus(order = new_order)
                add_shipping.save()
                cart.user = request.user #users need to be logged in for this to work
                cart.active = False
                cart.save()
                del request.session['cart_id']
                del request.session['cart_items']
                return HttpResponseRedirect('/orders/')
    return render_to_response('cart/checkout.html', locals(), context_instance=RequestContext(request))