from django.db import models

# Create your models here.
from django.contrib.auth.models import User

from cart.models import Cart

from profiles.models import Address


STATUS_CHOICES = (
    ('Started', 'Started'),
    ('Abandoned', 'Abandoned'),
    ('Collected', 'Collected'),
)

class Order(models.Model):
    user = models.ForeignKey(User)
    cart = models.ForeignKey(Cart)
    order_id = models.CharField(max_length=120, default="ABC123")
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default='Started')
    address = models.ForeignKey(Address, null=True, blank=True)
    cc_four = models.CharField(max_length=4, null=True, blank=True)

    def __unicode__(self, ):
        return "Order number is %s" %(self.order_id)

SHIPPING_STATUS = (
    'Not Shipped', 'Not Shipped'
    'Shipping Soon', 'Shipping Soon'
    'Shipped', 'Shipped'
    )

class OrderShipmentStatus(models.Model):
    order = models.ForeignKey(Order)
    status = models.CharField(max_length=120, default='Not Shipped', choices='SHIPPING_STATUS')
    tracking_number = models.CharField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
     updated = models.DateTimeField(auto_now_add=False, auto_now=True)

     def __unicode__(self):
        return self.status