from django.db import models
from common.models import Basetable,Address
from locality.models import Locality
#from business.models import Business

from django.conf import settings as my_settings
import datetime
from django.db.models import Sum
from django.core.urlresolvers import reverse
from easy_thumbnails.fields import ThumbnailerImageField
from django.utils.translation import ugettext as _
from common.utils import getCoverPhoto
from django.template.loader import render_to_string
from gallery.models import PhotoAlbum

User = my_settings.AUTH_USER_MODEL
Gender = (
        ('M', _('Male')),
        ('F', _('Female')),
        ('R', _('Rather not say')),
)
import uuid
import os
def get_deal_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('deals', filename)

class DealCategory(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    created_on = models.DateTimeField(auto_now_add = True)
    modified_on = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User,related_name='dealcategory_createdby')
    modified_by = models.ForeignKey(User,related_name='dealcategory_modifiedby')
    def __unicode__(self):
        return self.name
    def get_deal_count(self):
        return Deal.objects.filter(category=self).count()
    
    
class Deal(Basetable):
    dealkey = models.CharField(max_length=4)
    deal_by = models.ManyToManyField(User,null=True)
    title = models.CharField(max_length=170)
    category = models.ForeignKey("DealCategory", null=True)
    #business = models.ForeignKey(Business,null=True,related_name="deal_business")
    original_price = models.FloatField(null=True)
    discount_price = models.FloatField(null=True)
    start_date = models.DateField(null=True)
    slug = models.CharField(max_length=200)
    address = models.ManyToManyField(Address,null=True)
    end_date = models.DateField(null=True)
    max_count = models.IntegerField(default=0)
    limit_per_customer = models.IntegerField(null=True)
    can_gifted = models.BooleanField(default=True)
    voucher_valid = models.DateField(null=True)
    about = models.TextField(null=True)
    hihlights = models.TextField(null=True)
    fineprint = models.TextField(null=True)
    most_viewed = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default = False)
    seo_title = models.CharField(max_length=200, null=True)
    seo_description = models.CharField(max_length=400, null=True)
    album = models.ForeignKey(PhotoAlbum, blank=True, null=True, on_delete=models.SET_NULL)
    merchant = models.ForeignKey(User, related_name="DealMerchant", null=True)
        
    def delete(self):
        super(Deal, self).delete()
    def get_visits(self):
        return self.most_viewed
    def get_action_type(self):
        if self.status=='P':return 'update'
        else:return 'delete'
    def get_payment_title(self):
        return self.title
    def get_discount(self):
        return int(round(100-(self.discount_price/self.original_price*100)))
    def get_savings(self):
        return int(self.original_price-self.discount_price)
    def get_revenue_generated(self):
        sold = self.get_total_reg_count()
        return {
            'total': sold * self.discount_price
        }
    #Notification
    def get_staff_preview_url(self):
        url = reverse('staff_deal_preview',args=[self.id])
        return url
    def get_preview_url(self):
        url = reverse('staff_deal_preview',args=[self.id])
        return url
    def get_modified_time(self):
        return self.modified_on
    def get_staff_listing_url(self):
        url = reverse('staff_deals_home')
        return url
    #Notification
    def get_first_deal_image(self):
        photo = getCoverPhoto(self)
        if photo:
            return photo.photo
        else:
            if self.album:
                return self.album.get_cover_image()
            else:
                return False
    
    def get_default_image(self):
        return my_settings.STATIC_URL+"ui/images/global/img-none.png"      
    
    def get_todays_registered(self):
        now = datetime.datetime.now()
        return DealPayment.objects.filter(deal=self,created_on__year=now.year,created_on__month=now.month,created_on__day=now.day)
    
    def get_total_reg_count(self):
        drelation = DealPayment.objects.filter(deal=self).aggregate(limited_cnt=Sum('quantity'))
        if drelation['limited_cnt']:return drelation['limited_cnt']
        else:return 0 
    
    def get_total_percentage(self):
        now = datetime.datetime.now()
        drelation = DealPayment.objects.filter(deal=self).aggregate(limited_cnt=Sum('quantity'))
        if drelation['limited_cnt']: c= drelation['limited_cnt']
        else:c=0
        p = (c*1.0 / self.max_count*1.0)*100
        return int(p)
    
    def get_voucher_count(self):
        voucher = DealPayment.objects.filter(deal=self,status__in='[D,S]')
        if voucher:return voucher.count()
        else:return 0
    def get_voucher_used_count(self):
        voucher = DealPayment.objects.filter(deal=self,status = 'D')
        if voucher:return voucher.count()
        else:return 0    
    def get_count_blocked_voucher(self):
        voucher = DealPayment.objects.filter(deal=self,status = 'B')
        if voucher:return voucher.count()
        else:return 0  
    def get_count_pending_voucher(self):
        voucher = DealPayment.objects.filter(deal=self,status = 'S')
        if voucher:return voucher.count()
        else:return 0  
   
    def get_count_total_sold(self):
        drelation = DealPayment.objects.filter(deal=self).aggregate(limited_cnt=Sum('quantity'))
        if drelation['limited_cnt']:
            return drelation['limited_cnt']
        else:
            return 0
    def get_count_used_deals(self):
        drelation = DealPayment.objects.filter(deal=self,status = 'D').aggregate(limited_cnt=Sum('quantity'))
        if drelation['limited_cnt']:
            return drelation['limited_cnt']
        else:
            return 0
    def get_count_pending_deals(self):
        drelation = DealPayment.objects.filter(deal=self,status = 'S').aggregate(limited_cnt=Sum('quantity'))
        if drelation['limited_cnt']:return drelation['limited_cnt']
        else:return 0
    
    def get_count_remaining_deals(self):
        drelation = DealPayment.objects.filter(deal=self).aggregate(limited_cnt=Sum('quantity'))
        if drelation['limited_cnt']:
            total = self.max_count - drelation['limited_cnt']
            return total
        else:return self.max_count   
           
    def get_remaining_scnd(self):
        from deal.utils import get_rem_seconds
        today = datetime.date.today()
        return get_rem_seconds(self,today)
    
    def get_remaining_second(self):
        today = datetime.date.today()
        valid = self.voucher_valid
        if valid>today:
            a = valid-today
            return str(a.days)+' days'
        else:return _('Expired')
    
    def get_photos(self):
        if self.album:
            return self.album.get_gallery_uploaded_images()
        return None   
    
    def get_absolute_url(self):
        url = '/deals/'+ self.slug+'.html'
        return url
    def get_email_absolute_url(self):
        url ='/deals/'+self.slug+'.html'
        return url
   
    def get_full_url(self):
        return '%sdeals/?id=%d'%(my_settings.WEBSITE_URL,self.id)
    
    def get_deal_relation_info(self):
        return DealRelation.objects.get(deal=self)
    def get_search_result_html( self ):
        template = 'search/r_deals.html'
        data = { 'object': self }
        return render_to_string( template, data )
     
    class Meta:
        permissions = (("publish_deals", "Can Publish Deals"),("promote_deals", "Can Promote Deals"),)   
   
    def __unicode__(self):
        return self.title

# class DealPhotos(models.Model):
#     deal = models.ForeignKey("Deal",null=True, related_name = "deal_images")
#     title = models.CharField(max_length=200,null=True)
#     photo = ThumbnailerImageField(upload_to=get_deal_path,resize_source=dict(size=(700, 0), crop='smart'),)
#     uploaded_by = models.ForeignKey(User,related_name='deal_photos_uploaded_by',null=True)
#     uploaded_on  = models.DateTimeField( auto_now_add = True)
#     def __unicode__(self):
#         return self.title
#     
#     def get_delete_url(self):
#         return reverse('staff_deal_delete_photos', args=[self.id])

class Faqs(models.Model):
    created_on = models.DateField(auto_now_add=True)
    question = models.CharField(max_length=500,null=True,blank=True)
    answer = models.TextField(null=True,blank=True)
    
class How(models.Model):
    created_on = models.DateField(auto_now_add=True)
    heading = models.CharField(max_length=100,null=True,blank=True)
    content = models.TextField(null=True,blank=True)

class GiftedAddress(models.Model):
    g_name = models.CharField(max_length=100)
    g_mobile = models.CharField(max_length=20,null=True)
    g_email = models.EmailField(null=True)
    g_message = models.TextField(null=True)
    
class Subscribe(models.Model):
    created_on = models.DateField(auto_now_add=True)
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=20,null=True,blank=True)
    created_by = models.ForeignKey(User,related_name="DealsubscribeUser",null=True)
    
    
class DealPayment(models.Model):
    #Deal Info
    deal = models.ForeignKey('Deal',related_name="dealpayment")
    unit_price = models.FloatField(null=True)
    quantity = models.IntegerField(default=0)
    quantity_static = models.IntegerField(default=1)
    total_price = models.FloatField(null=True)
    dealkey = models.CharField(max_length=20)
    is_friend = models.BooleanField(default=False)
    gift_addr = models.ForeignKey('GiftedAddress',null=True,blank=True )
    
    status = models.CharField(max_length=1,default='P')#P = Not Buy   S = Bought and Pending D = Delivered E=Payment Failed  W=Waiting
    delivered_date = models.DateTimeField(null=True)
    #User Info
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add = True)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20,null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=500,null=True)
    
    #Payment Details
    is_paid = models.BooleanField(default=False)
    transaction_no = models.CharField(max_length=200,null=True)
    payment_status = models.CharField(max_length=200,null=True)
    payer_status = models.CharField(max_length=200,null=True)
    transaction_type = models.CharField(max_length=200,null=True)
    
