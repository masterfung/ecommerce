from django.db import models
from django.contrib.auth.models import User


from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self, ):
        return str(self.id)
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart)
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self, ):
        return str(self.cart.id)
