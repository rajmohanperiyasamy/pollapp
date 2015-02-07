from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_countries import CountryField

from bmshop.shop.settings import *
from common.models import Basetable
from easy_thumbnails.fields import ThumbnailerImageField 
User = settings.AUTH_USER_MODEL


class Shop(Basetable):
    notification_emails = models.TextField()
    default_country = CountryField()
    is_taxes = models.BooleanField(default=False)
    tax_value = models.FloatField(default=0.0)
    meta_title = models.CharField(blank=True, max_length=200)
    meta_description = models.TextField(blank=True)

    def __unicode__(self):
        return self.meta_title
    
    @classmethod
    def get_shop_settings(cls):
        try:
            return Shop.objects.all()[:1][0]
        except:
            return Shop()
        
class Discount(Basetable):
    name = models.CharField( max_length=100)
    value = models.FloatField()
    type = models.PositiveSmallIntegerField(choices=DISCOUNT_TYPE_CHOICES, default=DISCOUNT_TYPE_ABSOLUTE)
    
    def __unicode__(self):
        return self.name

    
class PymentSettings(models.Model):
    paypal = models.BooleanField(default=False)
    googlecheckout = models.BooleanField(default=False)
    cash_on_delivery = models.BooleanField(default=False)
    
    def __unicode__(self):
        return 'pay_settings'   
    
    @classmethod
    def get_pay_settings(cls):
        try:
            return PymentSettings.objects.all()[:1][0]
        except:
            return PymentSettings()

class Shipping(models.Model):
    active = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    price = models.FloatField(default=0.0)
    
    def __unicode__(self):
        return self.name
        
    @classmethod
    def get_shippment_settings(cls):
        try:
            return Shipping.objects.all()[:1][0]
        except:
            return Shipping()