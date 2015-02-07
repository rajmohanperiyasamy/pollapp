from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
User = settings.AUTH_USER_MODEL

class StripePlanDetails(models.Model):
    name = models.CharField(max_length=50,null=True)
    plan_id = models.CharField(max_length=40,unique = True)
    currency = models.CharField(max_length=3)
    amount = models.FloatField(max_length=20)
    interval = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add = True,null=True)
    type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name
    
    def get_customer_count(self):
        try:
            count = StripePaymentDetails.objects.filter(plan_id=self).count()
        except:
            from sys import exc_info
            print exc_info()
            count = 0
        return count
        
class StripePaymentDetails(models.Model):
    user =  models.ForeignKey(User,null=True,related_name='stripe_payment_createdby')
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    customer_id = models.CharField(max_length=200)
    module = models.CharField(max_length=20)
    subscription_id = models.CharField(max_length=40)
    plan_id = models.ForeignKey(StripePlanDetails,null=True,related_name='stripe_user_subscription')
    created_on = models.DateTimeField(auto_now_add = True,null=True)
    email_id = models.EmailField(max_length=200)
    subscription_status = models.CharField(max_length=20)
    
    def __unicode__(self):
        #return self.content_object.__unicode__()
        return self.subscription_id
    
    def get_unsubscribe_request(self):
        try:return StripeUnsubscribers.objects.get(stripe_details = self)
        except:False
        
        
class StripeUnsubscribers(models.Model):
    stripe_details = models.ForeignKey(StripePaymentDetails)
    staff = models.ForeignKey(User,null=True)
    unsubscribed_on = models.DateField(null = True,auto_now_add = True)
    reason = models.CharField(null=True, max_length = 200)
    mobile = models.CharField(null=True, max_length = 20)
    email = models.EmailField(null=True, max_length = 50)
    
    def __unicode__self(self):
        return self.stripe_details.subscription_id
    
    
    
    