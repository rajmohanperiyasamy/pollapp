import datetime
import uuid
import os

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import fields
from django.template.loader import render_to_string
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.conf import settings

from gallery.models import PhotoAlbum
from locality.models import Locality
from common.utils import get_global_settings
from common.utils import getCoverPhoto
from common.models import ModuleNames,Basetable, Address

from audit_log.models.managers import AuditLog

User = settings.AUTH_USER_MODEL

def get_classifdlogo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('classifd/log', filename)
def get_classifdgallery_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('classifd/images', filename)

class ClassifiedCategory(models.Model):
    name = models.CharField(max_length=60)
    parent = models.ForeignKey('self',null=True,related_name='parentcategory')
    type_order = models.IntegerField(null=True,default=1)
    sp_price = models.FloatField(default=0.0)
    slug = models.CharField(max_length=200,null=True)
    is_rent = models.BooleanField(default=False)
    seo_title = models.CharField(max_length=150,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    
    def __unicode__(self):
        return self.name
    def get_category(self):
        return ClassifiedCategory.objects.filter(parent=self)
    def get_child_category(self):
        return ClassifiedCategory.objects.filter(parent=self).order_by('name')
    def getChildCategory(self):
        return ClassifiedCategory.objects.filter(parent=self)
    def get_strid(self):
        return str(self.id)
    def get_attribute(self):
        return ClassifiedAttribute.objects.filter(category=self.id)
    def get_attr_count(self):
        return ClassifiedAttribute.objects.filter(category=self.id).count()
    def get_classifieds_count(self):
        return Classifieds.objects.filter(category__parent= self.id,status='P').count()
    def get_classifieds_count_subcat(self):
        return Classifieds.objects.filter(category= self.id,status='P').count()
    def get_expired_count(self):
        return Classifieds.objects.filter(category = self.id, status='E').count()
    def get_absolute_url(self):
        return '/classifieds/%s/' % (self.slug)

def get_default_category():
    parent = ClassifiedCategory.objects.get_or_create(name="Uncategorized", slug='nocategory')[0]
    return ClassifiedCategory.objects.get_or_create(name="Uncategorized", slug='uncategorized', parent=parent)[0]

ATTRIBUTE_TYPE = (
    ("K", "Check Box"),
    ("R", "Radio Button"),
    ("S", "Select Box"),
    ("C", "Text Field"),
)

class ClassifiedAttribute(models.Model):
    name = models.CharField(max_length=70)
    sell = models.BooleanField()
    buy  = models.BooleanField()
    rent = models.BooleanField()
    rent_out = models.BooleanField()
    category = models.ForeignKey("ClassifiedCategory")
    default_values = models.TextField(null=True)
    type = models.CharField(max_length=1,choices=ATTRIBUTE_TYPE,default='C')#C=CharField    K=Checkbox    S=Combobox    R=Radiobutton    T=Textbox    I=Filefield
    
    def __unicode__(self):
        return self.name
    
    def get_default_values(self):
        if self.type == 'K' or self.type == 'S' or self.type == 'R':
            v = self.default_values.split(':|')
        else:
            v = [self.default_values]
        return v
    
    def get_cls_count(self):
        if self.type == 'K' or self.type == 'S' or self.type == 'R':
            b = []
            vals = self.default_values.split(':|')
            for val in vals:
                cnt = ClassifiedAttributevalue.objects.filter(attribute_id=self,value__icontains=val,classified__status='P').count()
                a = {'value':val,'count':cnt}
                b.append(a)
            return b
        else:pass


class Classifieds(Basetable):
    title = models.CharField(max_length=110)
    description = models.TextField()
    category = models.ForeignKey("ClassifiedCategory", related_name='cls_category', default=get_default_category, on_delete=models.SET_DEFAULT)
    #expires_on =  models.DateTimeField()
    action = models.CharField(max_length = 1)#B=buy,S=sell,R=rent,O=rent_out
    most_viewed = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField("Tag",null=True)
    data_src = models.CharField(max_length=10,null=True)
    source_url = models.CharField(max_length=400,null=True)
    tp_id = models.CharField(max_length=20,null=True)# is third party
    slug=models.SlugField(max_length=160) 
    classified_price = models.FloatField(default=0.0,null=True)
    
    payment = models.ForeignKey("ClassifiedPrice",null=True,blank=True)
    listing_type = models.CharField(max_length=1,null=True)# Featured=>F or Sponsored =>S or Basic=>B
    price = models.CharField(max_length=14,default=0)#LISTING PRICE
    listing_start_date = models.DateTimeField(null=True) 
    listing_end_date = models.DateTimeField(null=True) 
    is_paid = models.BooleanField(default = False)
    
    album = models.ForeignKey(PhotoAlbum, blank=True, null=True, on_delete=models.SET_NULL)
    
    seo_title = models.CharField(max_length=150,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    
    address = models.ForeignKey(Address,null=True)
    published_on = models.DateTimeField(null=True,blank=True)
    
    audit_log = AuditLog()
    
    def __unicode__(self):
        return self.title
    
    def get_visits(self):
        return self.most_viewed
    
    def get_action_type(self):
        if self.status=='P':return 'update'
        else:return 'delete'
        
    def get_status(self):
        if self.status =='P':
            sts = 'published'
        elif self.status =='N':
            sts = 'pending' 
        elif self.status =='B':
            sts = 'blocked'
        elif self.status =='R':
            sts = 'rejected' 
        elif self.status =='E':
            sts = 'expired' 
        else: sts = 'drafted' 
        return sts 
    
    def get_offline_payment_object(self):
        ctype = ContentType.objects.get_for_model(self)
        try:
            from payments.models import OfflinePayment
            payobj = OfflinePayment.objects.filter(
                content_type=ctype,
                object_id=self.id,
            ).order_by('-posted_date')[0]
            return payobj
        except:
            return False
    
    def get_preview_url(self):
        return reverse('staff_preview_classified', args=[self.id]) 
    def get_modified_time(self):
        return self.modified_on
    def get_attribute_values(self):
        return ClassifiedAttributevalue.objects.filter(classified = self.id,value__isnull=False).exclude(value='')
    
    def get_photos(self):
        if self.album:
            return self.album.get_gallery_uploaded_images()
        return None
    
    def get_photo_gallery(self):
        return self.get_photos()
    
    def get_absolute_url(self):
        if not self.tp_id:
            url = '/classifieds/'+self.slug+'.html'
        else:
            url = '/classifieds/tp/'+self.tp_id
        return url
    
    def get_staff_preview_url(self):
        url = reverse('staff_preview_classified',args=[self.id])
        return url
    
    def get_staff_listing_url(self):
        url = reverse('staff_classified_home')
        return url
    
    def get_price(self):
        if self.price == '0':
            return False
        else:
            self.price
    
    def get_payment_photo(self):
        return self.get_first_classified_photo()
    
    def get_payment_title(self):
        return self.title    
    
    def get_payment_description(self):
        if self.description:
            return self.description
        else:
            return self.title
    
    def get_payment_status(self):
        if self.is_paid:
            return True
        else:
            return False    
    
    def get_first_classified_photo(self):
        photo = getCoverPhoto(self)
        if photo:
            return photo.photo
        else:
            if self.album:
                return self.album.get_cover_image()
            else:
                return False
    
    def get_default_image(self):
        return settings.STATIC_URL+"ui/images/global/img-none.png"        
    
    def get_comments_count(self):
        return ClassifiedComment.objects.filter(classified=self).count()
    def get_comments(self):
        return ClassifiedComment.objects.filter(classified=self,status='A').order_by('-id') #-created_on
    def get_total_comments_count(self):
        return ClassifiedComment.objects.filter(classified=self).count()
    def get_pending_comments_count(self):
        return ClassifiedComment.objects.filter(classified=self,status='N').count()
    def get_rejected_comments_count(self):
        return ClassifiedComment.objects.filter(classified=self,status='B').count()
    def get_approved_comments_count(self):
        return ClassifiedComment.objects.filter(classified=self,status='A').count()
    def get_classified_list( self ):
        if not self.tp_id:
            template = 'default/classifieds/o_classified.html'
        else:
            template = 'classifieds/customer/tp_classified.html'
        data = { 'clas': self }
        return render_to_string( template, data )
    def get_tp_attributes(self):
        return TPClassifiedsAttribute.objects.filter(classified=self).exclude(attr_name__in=['price','has_photo','user_id'])
    def get_tp_first_images(self):
        try:
            photo= TPClassifiedsImages.objects.filter(classified=self).exclude(img_size='s').order_by('-img_size')[:1]
            return photo[0]
        except:
            return None
    def get_tp_images(self):
        return  TPClassifiedsImages.objects.filter(classified=self).exclude(img_size='s')
        
    def get_tp_thumb_images(self):
        return TPClassifiedsImages.objects.filter(classified=self,img_size='s')
    def get_tp_thumb_image(self):
        try:
            photo=TPClassifiedsImages.objects.filter(classified=self,img_size='s')[:1]
            return photo[0]
        except:
            pass
    def get_search_result_html( self ):
        template = 'search/r_classifieds.html'
        data = { 'object': self }
        return render_to_string( template, data )
    def save(self):
        try:
            price = self.get_price()
            if price:
                self.price = val
            super(Classifieds,self).save()
        except:
            return True
    def tp_save(self):
            super(Classifieds,self).save()
    def get_reportid(self):
        try:
            report = ClassifiedReport.objects.filter(classified=self)[:1]
            for rep in report:
                return rep.id
        except:pass
    def get_tag(self):
        return self.tags.all()
    def get_watch(self):
        return self.watchlist.all()
    def get_price(self):
        try:
            price = ClassifiedAttributevalue.objects.get(classified = self.id,attribute__icontains='price')
            return price           
        except:
            return False
         
    def get_offensive_classifieds_report(self):
        return ClassifiedReport.objects.filter(report='O',classified=self.id).count()
    #def getOffensiveFilter(self):
    #    return self.objects.filter(report='O')
    def get_spam_classifieds_report(self):
        return ClassifiedReport.objects.filter(report='S',classified=self.id).count()
    def get_old_classifieds(self):
        return ClassifiedReport.objects.filter(report='L',classified=self.id).count()
    
    def get_changes_between_objects(object1, object2, excludes=[]):
        """
        Finds the changes between the common fields on two objects
    
        :param object1: The first object
        :param object2: The second object
        :param excludes: A list of field names to exclude
        """
        changes = {}
    
        # For every field in the model
        for field in object1._meta.fields:
            # Don't process excluded fields or automatically updating fields
            if not field.name in excludes and not isinstance(field, fields.AutoField):
                # If the field isn't a related field (i.e. a foreign key)..
                if not isinstance(field, fields.related.RelatedField):
                    old_val = field.value_from_object(object1)
                    new_val = field.value_from_object(object2)
                    # If the old value doesn't equal the new value, and they're
                    # not both equivalent to null (i.e. None and "")
                    if old_val != new_val and not(not old_val and not new_val):
                        changes[field.verbose_name] = (old_val, new_val)
    
                # If the field is a related field..
                elif isinstance(field, fields.related.RelatedField):
                    if field.value_from_object(object1) != field.value_from_object(object2):
                        old_pk = field.value_from_object(object1)
                        try:
                            old_val = field.related.parent_model.objects.get(pk=old_pk)
                        except field.related.parent_model.DoesNotExist:
                            old_val = None
    
                        new_pk = field.value_from_object(object2)
                        try:
                            new_val = field.related.parent_model.objects.get(pk=new_pk)
                        except field.related.parent_model.DoesNotExist:
                            new_val = None
    
                        changes[field.verbose_name] = (old_val, new_val)
        return changes
    class Meta:
        permissions = (("publish_classifieds", "Can Publish Classifieds"),("promote_classifieds", "Can Promote Classifieds"),)   


class ClassifiedAttributevalue(models.Model):
    classified = models.ForeignKey("Classifieds",related_name='val_cls')
    attribute = models.CharField(max_length=100)
    value = models.TextField()
    attribute_id = models.ForeignKey("ClassifiedAttribute",related_name='val_atr')
    
    def __unicode__(self):
        return self.attribute
    
class Tag(models.Model):  
    tag = models.CharField(max_length=50)  # tagname  
    def __unicode__(self):
        return self.tag
    class Admin:  
        pass


class ClassifiedNotification(models.Model):
    email = models.EmailField()
    skey = models.CharField(max_length=100)
    date = models.DateTimeField()
    created_on = models.DateTimeField('createdon', auto_now_add=True)
    

class ClassifiedReport(models.Model):
    report = models.CharField(max_length=1)#offensive=O spam=S oldad=L 
    report_by = models.ForeignKey(User)
    classified = models.ForeignKey("Classifieds",related_name = 'report')
    def __unicode__(self):
        return self.report
    

class Watchlist(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    classifieds = models.ManyToManyField('Classifieds')
    def get_list(self):
        return self.classifieds.all()

    
class ClassifiedComment(models.Model):
    classified = models.ForeignKey("Classifieds")
    name = models.CharField(max_length=60,null=True)
    email = models.EmailField(max_length=300,null=True)
    title = models.CharField(max_length=120,null=True)
    comment = models.TextField()
    abuse_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=1,default='A')#N=new    B=blocked    A=approved
    approved_on = models.DateTimeField("CC_approvedoncomment", auto_now = True)
    created_by = models.ForeignKey(User, related_name='createdbyclassifiedmcomment',null=True)
    created_on  = models.DateTimeField('Created', auto_now_add = True)
    
"""
    Classifieds Tables used to save from third party website
"""   

        

class TPClassifiedsImages(models.Model):
    classified = models.ForeignKey("Classifieds")
    img_url = models.CharField(max_length=250,null=True)
    img_size = models.CharField(max_length=10,null=True)
    img_width = models.CharField(max_length=4,null=True)
    img_height = models.CharField(max_length=4,null=True)
    img_alt = models.CharField(max_length=150,null=True)
    
        
class TPClassifiedsAttribute(models.Model):
    classified = models.ForeignKey("Classifieds")
    attr_name = models.CharField(max_length=100,null=True)
    attr_val = models.CharField(max_length=250,null=True)
    def get_attr_name(self):
        return self.attr_name.replace('_',' ')
   
class ClassifiedPrice(models.Model):
    level = models.CharField(max_length=10,null=True)
    level_visibility = models.BooleanField(default=True)
    level_label = models.CharField(max_length=50,null=True)   
    is_paid = models.BooleanField(default=True)
    
    exposure = models.CharField(max_length=2,null=True)
    images=models.CharField(max_length=1,null=True)#Y=Yes N=No E=None
    comments = models.CharField(max_length=1, null=True) #Y=yes N=No E=None
    share_buttons= models.CharField(max_length=1,null=True)#Y=Yes N=No E=None
    sms=models.CharField(max_length=1,null=True)#Y=Yes N=No E=None
    newsletter=models.CharField(max_length=1,null=True)#Y=Yes N=No E=None
    social_media=models.CharField(max_length=1,null=True)#Y=Yes N=No E=None
    
    contract_period = models.IntegerField(default=0)  
    contract_period_option = models.CharField(max_length=10,null=True)
    price = models.FloatField(default=0.0)
    
    def get_exposure(self):
        if self.exposure=='1':return _('1X') 
        elif self.exposure=='2':return _('5X') 
        elif self.exposure=='3':return _('10X') 
        elif self.exposure=='4':return _('15X') 
        elif self.exposure=='5':return _('20X') 
        elif self.exposure=='6':return _('25X')
        else:return _('Standard')
        
class OodleSettings(models.Model):
    api_key     = models.CharField(max_length=20)
    radius      = models.IntegerField(default=15)
    location    = models.CharField(max_length=50,null=True)
    region      = models.CharField(max_length=20,null=True)
    def __unicode__(self):
        return 'Oodle Settings'
