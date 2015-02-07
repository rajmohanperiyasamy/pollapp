from django.db import models
from django.utils.translation import ugettext_lazy as _

from bmshop.products.models import Product
from bmshop.order.settings import *
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Order(models.Model):
    
    order_number = models.CharField(max_length=30)
    user = models.ForeignKey(User, verbose_name=_(u"User"), blank=True, null=True)
    session = models.CharField(blank=True, max_length=100)

    created = models.DateTimeField(auto_now_add=True)

    status = models.PositiveSmallIntegerField(_(u"State"), choices=ORDER_STATES, default=SUBMITTED)
    state_modified = models.DateTimeField(auto_now_add=True)

    price = models.FloatField(default=0.0)
    tax = models.FloatField(default=0.0)

    #Address
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(null=True, blank=True, max_length=100)
    state = models.CharField(null=True, blank=True, max_length=100)
    zip_code = models.CharField(null=True, blank=True, max_length=100)
    country = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(blank=True, max_length=20)

    #Shipping
    shipping_method = models.CharField(max_length=50, null=True, blank=True)
    shipping_price = models.FloatField(default=0.0)

    #Payment
    payment_method = models.CharField(max_length=50,choices=PAYMENT_MODE,default=NOT_PAID)
    payment_price = models.FloatField(default=0.0)

    voucher_number = models.CharField(blank=True, max_length=100)
    voucher_price = models.FloatField(default=0.0)

    message = models.TextField(blank=True)
    pay_link = models.TextField(blank=True)
    transaction_id = models.TextField(_(u"Transaction Id"), blank=True)

    delivery_status = models.CharField(max_length=5,choices=DELIVERY_STATUS,default=NOT_DELIVERED)
    delivery_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ("-created", )

    def __unicode__(self):
        return "(%s - %s - %s)" % (self.order_number, self.name, self.payment_method)

    def get_order_items(self):
        return self.order_items.order_by('-id')
    

class OrderItem(models.Model):
    order = models.ForeignKey("Order", related_name="order_items")
    price = models.FloatField(default=0.0)
    tax = models.FloatField(default=0.0)
    quantity = models.FloatField(blank=True, null=True)

    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.SET_NULL)
    product_uid = models.CharField(blank=True, max_length=100)
    product_name = models.CharField(blank=True, max_length=100)
    product_price = models.FloatField(default=0.0)
   
    def __unicode__(self):
        return "%s" % self.product_name
    
    