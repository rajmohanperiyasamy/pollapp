from django.db import models
from django.utils.translation import ugettext_lazy as _

from bmshop.products.models import Product
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Address(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    firstname = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    zip_code = models.CharField( max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(blank=True, max_length=20)

    def __unicode__(self):
        return "%s / %s" % (self.address, self.city)
    
class Wishlist(models.Model):
    products_id = models.PositiveIntegerField(null=False)
    added_on = models.DateTimeField(null=False)
    added_by = models.ForeignKey(User,null=True)
    
    
        

  
    
    
    
    