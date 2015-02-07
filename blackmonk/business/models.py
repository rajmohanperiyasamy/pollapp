from datetime import datetime
from django.conf import settings as my_settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
import os
import uuid

from audit_log.models.managers import AuditLog
from common.models import Basetable, Address
from easy_thumbnails.fields import ThumbnailerImageField
from gallery.models import PhotoAlbum
from locality.models import Locality
from payments.stripes.models import StripePaymentDetails

User = my_settings.AUTH_USER_MODEL

def get_bizlogo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('biz/logo', filename)

def get_bizgallery_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('biz/images', filename)

def get_bizfile_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('biz/files', filename)

COUPON_OFFER_TYPE=(('C',_('Coupon')),('O',_('Offer')))

class Tag(models.Model):
    tag = models.CharField(max_length=150)

    def __unicode__(self):
        return self.tag

class BusinessCategory(models.Model):
    name = models.CharField(max_length=120)
    parent_cat = models.ForeignKey("BusinessCategory", null=True,related_name='parentcategory')
    slug = models.SlugField(max_length=150)
    seo_title = models.CharField(max_length=200,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    price_year = models.FloatField(null=True,default=0.0)
    price_month = models.FloatField(null=True,default=0.0)

    def __unicode__(self):
        return self.name
    def getMainCategory(self):
        return BusinessCategory.objects.filter(parent_cat__isnull=True).order_by('name')
    def get_category(self):
        return BusinessCategory.objects.filter(parent_cat=self.id).order_by('name')
    def getChildCategory(self):
        clist = BusinessCategory.objects.filter(parent_cat=self.id).order_by('name')
        if not clist.exists():
            BusinessCategory.objects.create(
                name=self.name,
                parent_cat=self,
                slug=self.slug + "-default",
                seo_title=self.seo_title,
                seo_description=self.seo_description,
                price_year=self.price_year,
                price_month=self.price_month
            )
            clist = BusinessCategory.objects.filter(parent_cat=self.id).order_by('name')
        return clist
    def get_child_business_count(self):
        if self.parent_cat:
            return Business.objects.filter(categories__id=self.id).count()
        else:
            return Business.objects.filter(categories__parent_cat=self).distinct().count()
    def get_business_count(self):
        return Business.objects.filter(is_active=True, status='P', category=self).count()
    def get_all_business_count(self):
        return Business.objects.filter(categories__id=self.id).exclude(status='D').count()
    def get_absolute_url(self):
        return '/business/' + self.slug + '/'
    def get_attributes_combobox(self,style=False):
        if self.parent_cat:
            return Attributes.objects.filter(Q(type='S')|Q(type='K')|Q(type='R'),(Q(category = self)|Q(category = self.parent_cat))).order_by('-name')
        else:
            return Attributes.objects.filter(Q(type='S')|Q(type='K')|Q(type='R'),category = self).order_by('-name')
    class Meta:
        ordering = ["name"]

attributeType = (
          ('K', 'CheckBox'),
          ('R', 'Radio Button'),
          ('S', 'Select Box'),
          ('C', 'Text Field'),
          #('I', 'File/Image'),
)
display_position=(
        ('C', 'Center'),
        ('L', 'Left'),
        ('R', 'Right'),
)


class AttributeGroup(models.Model):
    name = models.CharField(max_length=120)#Features, Facilities, Services ...etc
    order_by=models.IntegerField(default=1)
    display_position = models.CharField(max_length=1,default='C')#C=center    L=left    R=right
    #style = models.CharField(max_length=1,default='A',choices=attributeStatus)#A=attribute    S=service    P=payment    W=workingHours    This for service and attribute

    def __unicode__(self):
        return self.name

    def get_attributes(self,category):
        return Attributes.objects.filter(attribute_group=self,category=category).order_by('type')
    def get_sub_attributes_all(self):
        return Attributes.objects.filter(attribute_group=self)

    def get_payment_methods(self):
        return PaymentOptions.objects.all()
    def get_business_attributes(self):
        return BizAttributes.objects.filter(attribute=self)
    def get_business_services(self):
        return BizServices.objects.filter(attribute=self)


class Attributes(models.Model):
    name = models.CharField(max_length=120)
    attribute_group = models.ForeignKey("AttributeGroup")
    category = models.ForeignKey("BusinessCategory")
    type = models.CharField(max_length=1,choices=attributeType)#C=CharField    K=Checkbox    S=Combobox    R=Radiobutton    T=Textbox    I=Filefield
    staff_created = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
    def get_default_values(self):
        return AttributeValues.objects.filter(attribute_key=self,staff_created=True)
    def get_type(self):
        if self.type == 'C':return 'Text Field'
        elif self.type == 'S':return 'Select Box'
        elif self.type == 'K':return 'Check Box'
        elif self.type == 'R':return 'Radio button'
        else:return '-- not selected --'


class AttributeValues(models.Model):
    attribute_key = models.ForeignKey("Attributes",related_name='attributekey')
    staff_created = models.BooleanField(default=False)
    name = models.CharField(max_length=150)

    def __unicode__(self):
        return self.name
    def get_business_attributes(self):
        return BizAttributes.objects.filter(value__id=self.id,business__status='P')
    def get_business_count(self):
        return BizAttributes.objects.filter(value__id=self.id,business__status='P').distinct().count()

class BizAttributes(models.Model):
    business = models.ForeignKey("Business",related_name='bizattributes')
    key = models.ForeignKey("Attributes",related_name='bizattributeskey') #CharField(max_length=150)
    value = models.ManyToManyField("AttributeValues",related_name='bizattributesvalues') #color-red,blue...etc
    textbox_value=models.CharField(max_length=200,null=True,blank=True)

    def get_values(self):
        return self.value.all()


class WorkingHours(models.Model):
    notes = models.CharField(max_length=150, null=True)
    mon_start = models.CharField(max_length=30, null=True)
    mon_end = models.CharField(max_length=30, null=True)
    tue_start = models.CharField(max_length=30, null=True)
    tue_end = models.CharField(max_length=30, null=True)
    wed_start = models.CharField(max_length=30, null=True)
    wed_end = models.CharField(max_length=30, null=True)
    thu_start = models.CharField(max_length=30, null=True)
    thu_end = models.CharField(max_length=30, null=True)
    fri_start = models.CharField(max_length=30, null=True)
    fri_end = models.CharField(max_length=30, null=True)
    sat_start = models.CharField(max_length=30, null=True)
    sat_end = models.CharField(max_length=30, null=True)
    sun_start = models.CharField(max_length=30, null=True)
    sun_end = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=1, default='P')#P=published    H=private    D=draft

class BusinessLogo(models.Model):
    logo  = ThumbnailerImageField(upload_to=get_bizlogo_path,resize_source=dict(size=(300, 0), crop='smart'), null=True)
    uploaded_on = models.DateTimeField('createdonbusinesslogo', auto_now_add=True)
    uploaded_by=models.ForeignKey(User,null=True)

    def get_delete_url(self):
        return reverse('business_delete_logo', args=[self.id])

class Business(Basetable):
    #status P=publish    H=inactive    D=draft    N=new
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150)
    logo=models.OneToOneField("BusinessLogo",null=True,on_delete=models.SET_NULL)
    categories = models.ManyToManyField("BusinessCategory",related_name='allcategories',null=True)
    paymentoptions = models.ManyToManyField("PaymentOptions",related_name='business_paymentoptions',null=True)
    operating_hours = models.BooleanField(default=False)
    workinghours=models.OneToOneField("WorkingHours",null=True)
    tags = models.ManyToManyField("Tag",null=True)
    summary = models.CharField(max_length=600,null=True)
    description = models.TextField(null=True)

    #specialofferimage = models.URLField(null=True)
    #specialofferurl = models.URLField(null=True)
    #introductions = models.CharField(max_length=120,null=True)

    votes = models.PositiveIntegerField(default=0)
    ratings = models.FloatField(default=0)#ratings = models.PositiveIntegerField(default=0)
    most_viewed = models.PositiveIntegerField(default=0)
    seo_title = models.CharField(max_length=200,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    featured_sponsored = models.CharField(max_length=1,null=True,default='B')#F=Featured    S=Sponsored   B=Basic/Free
    sp_cost = models.FloatField(null=True) #listin price
    lstart_date = models.DateTimeField(null=True)
    lend_date = models.DateTimeField(null=True)
    payment =  models.ForeignKey("BusinessPrice",null=True)
    payment_type = models.CharField(max_length=1,null=True) #M-monthly , Y-yearly
    is_paid = models.BooleanField(default = False)
    fb_url = models.CharField(max_length=150,null=True)
    twitter_url= models.CharField(max_length=150,null=True)
    gooleplus_url = models.CharField(max_length=150,null=True)
    is_claimable = models.BooleanField(default = False)
    album = models.ForeignKey(PhotoAlbum, blank=True, null=True, on_delete=models.SET_NULL)
    audit_log = AuditLog()
    address = models.ManyToManyField(Address,null=True)

    def __unicode__(self):
        return self.name
    def get_visits(self):
        return self.most_viewed
    def get_action_type(self):
        if self.status=='P':return 'update'
        else:return 'delete'
    def get_preview_url(self):
        return reverse('staff_preview_business', args=[self.id])
    def get_modified_time(self):
        return self.modified_on
    def get_status(self):
        if self.status =='P':
            sts = 'published'
        elif self.status =='N':
            sts = 'pending'
        elif self.status =='D':
            sts = 'drafted'
        elif self.status =='R':
            sts = 'rejected'
        else: sts = 'blocked'
        return sts
    def get_claim_status(self):
        try:
            claim=BusinessClaim.objects.get(business=self)
            return claim.is_approved
        except:
            return True
    def get_attribute_values(self):
        return BizAttributes.objects.filter(business = self.id).order_by('key__attribute_group','key')

    def get_files(self):
        return BusinessFiles.objects.filter(business=self.id)
    def get_parent_cat(self):
        parent = None
        for c in self.categories.all():
            parent = c.parent_cat
            if parent is not None: break
        if parent is None:
            self.categories.clear()
            parent = BusinessCategory.objects.get_or_create(
                name='Uncategorized',
                slug='uncategorized_parent',
                parent_cat=None
            )[0]
            default_cat = BusinessCategory.objects.get_or_create(
                name='Uncategorized',
                slug='uncategorized_sub',
                parent_cat=parent
            )[0]
            self.categories.add(default_cat)
        return parent
    def delete(self):
        try:
            bc=BusinessCoupons.objects.filter(business=self)
            bc.delete()
        except:pass
        try:
            bpr=BusinessProducts.objects.filter(business=self)
            bpr.delete()
        except:pass
        super(Business, self).delete()
    class Meta:
        permissions = (("publish_business", "Can Publish Business"),("promote_business", "Can Promote Business"),)

    def primary_address(self):
        try:
            return self.address.all()[0]
        except:
            return None

    def get_lat_lang(self):
        addr = Address.objects.filter(business=self)[:1][0]
        data = {}
        if addr.lat: data['lat']= addr.lat
        else:data['lat']=None
        if addr.lon:data['lon']= addr.lon
        else:data['lon']=None
        return data

    def getcategories(self):
        return self.categories.all()
    def gettags(self):
        return self.tags.all()
    def getaddress(self):
        return Address.objects.filter(business=self).order_by('id')
    def getotheraddress(self):
        return Address.objects.filter(business=self,status='A').order_by('id')
    def get_reviews(self):
        return BusinessReview.objects.filter(business=self, status='A',parent__isnull=True).order_by('-id')
    def get_reviews_count(self):
        return BusinessReview.objects.filter(business=self, status='A').count()
    def get_pending_reviews_count(self):
        return BusinessReview.objects.filter(business=self,status='N').count()
    def get_rejected_reviews_count(self):
        return BusinessReview.objects.filter(business=self,status='B').count()
    def get_total_reviews(self):
         return BusinessReview.objects.filter(business=self.id).order_by('-id')
    def get_total_reviews_count(self):
         return BusinessReview.objects.filter(business=self.id).count()
    def get_parent_category(self):
        for cat in self.getcategories()[:1]:
            return cat.parent_cat
    def getrating(self):
        try:
            rv = self.ratings / self.votes
        except:
            rv = 0
        return rv
    def getratinglist(self):
        try:
            rv = self.ratings*1.0 / self.votes
        except:
            rv = 0.0
        i=0
        a=[]
        while i<5:
            if i<rv and rv<i+1:
                    a.append(1)
            elif i<rv:
                    a.append(2)
            else:
                    a.append(0)
            i = i+1
        return a
    def getalllocation(self):
        return Locality.objects.all().order_by('name')

    def get_first_business_photo(self):
        if self.album:
            return self.album.get_cover_image()
        else:return False

    def get_photo_gallery(self):
        if self.album:
            return self.album.get_photo_gallery()
        else:return False

    def get_first_photo_gallery(self):
        if self.album:
            return self.album.get_cover_image()
        else:return False
    def get_cover_image(self):
        if self.album:
            return self.album.get_cover_image()
        else:return False


    def get_attributes(self,style=False):
        categories = self.categories.all()
        ids = []
        for c in categories:
            ids.append(c)
            try:
                c.parent_cat.id
                ids.append(c.parent_cat)
            except:pass
        if not style:
            return Attributes.objects.filter(category__in = ids).order_by('-name')
        else:
            return Attributes.objects.filter(category__in = ids,style=style).order_by('-name')
    def get_attributes_values(self):
        return BizAttributes.objects.filter(business=self).order_by('id')
    def get_services(self):
        return BizServices.objects.filter(business=self)
    def getbrochure(self):
        try:
            return Brochure.objects.get(business=self)
        except:
            return None
    def getContactCount(self):
        return ContactDetails.objects.filter(business=self).count()
    def get_payment_options(self):
        return self.paymentoptions.all()
    def get_working_hours(self):
        return WorkingHours.objects.filter(business=self)
    def get_sponsored_list(self):
        return Sponsoredlist.objects.filter(business=self)
    def get_featured_list(self):
        return Featuredlist.objects.filter(business=self)
    def is_featured(self):
        fl = Featuredlist.objects.filter(business=self,status='P')
        for f in fl:
            return True
        return False
    def is_featured_sponsored(self):
        today = datetime.today()
        if self.featured_sponsored=='S': return 'S'
        elif self.featured_sponsored=='F' and self.lend_date >= today: return 'F'
        else: return 'B'

    def get_coupons(self):
        return BusinessCoupons.objects.filter(is_active=True,business=self)
    def get_products(self):
        return BusinessProducts.objects.filter(business=self).order_by('id')
    def get_absolute_url(self):
        url = '/business/' + self.slug + '.html'
        return url
    #Notification
    def get_staff_preview_url(self):
        url = reverse('staff_preview_business',args=[self.id])
        return url
    def get_staff_listing_url(self):
        url = reverse('staff_manage_business')
        return url
    #Notification
    def get_default_image(self):
        return my_settings.STATIC_URL+"ui/images/global/img-none.png"

    def get_search_result_html( self ):
        template = 'search/r_business.html'
        data = { 'object': self ,'STATIC_URL':my_settings.STATIC_URL}
        return render_to_string( template, data )

    def get_payment_status(self):
        if self.is_paid:
            return True
        else:
            return False

    def get_payment_photo(self):
        if self.logo:
            if self.logo.logo:return self.logo.logo
            else:return None
        else:return None


    def get_payment_title(self):
            return self.name


    def get_payment_description(self):
        if self.summary:
            return self.summary
        else:
            return self.name
    def get_payment_listing_price(self):
        return self.sp_cost

    def get_payment_duration_type(self):
        if self.payment_type=='M':return 'Month'
        elif self.payment_type=='Y':return 'Year'

    def get_payment_listing_type(self):
        return self.payment.level_label
    
    def get_stripe_subscription_object(self):
        s_objects = StripePaymentDetails.objects.filter(object_id=self.id).exclude(subscription_status='inactive')
        if s_objects.exists():
            return s_objects[0]
        else:
            return False
        
    def get_stripe_subscription_status(self):
        s_objects = StripePaymentDetails.objects.filter(object_id=self.id).exclude(subscription_status='inactive')
        print self.id, s_objects.exists()
        try:   
            if s_objects.exists():
                return s_objects[0].subscription_status
            else:
                return False
        except:return False

class BusinessFiles(models.Model):
    title = models.CharField(max_length=120,null=True)
    business = models.ForeignKey("Business",related_name='businessfile',null=True)
    file=models.FileField(upload_to=get_bizfile_path)
    uploaded_on = models.DateTimeField('createdonbusinessfile', auto_now_add=True)
    uploaded_by=models.ForeignKey(User,null=True)

    def get_delete_url(self):
        return reverse('business_delete_files', args=[self.id])

class BusinessReview(models.Model):
    business = models.ForeignKey("Business")
    parent = models.ForeignKey("BusinessReview",null=True)
    subject = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=300)
    review = models.TextField()
    ratings = models.PositiveSmallIntegerField(default=0, null=True)
    abuse_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=1,default='N')#N=new    B=blocked    A=approved
    approved_on = models.DateTimeField("approvedonbreview", auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='createdby',null=True)
    created_on = models.DateTimeField('Createdon',auto_now_add=True)
    def get_ratings_percent(self):
        return self.ratings*20
    def get_child(self):
        return BusinessReview.objects.filter(parent=self)


class PaymentOptions(models.Model):
    name = models.CharField(max_length=100)
    image_position=models.CharField(max_length=200,null=True)

    def __unicode__(self):
        return self.name


class ContactDetails(models.Model):
    business = models.ForeignKey("Business")
    name = models.CharField(max_length=50,null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20,null=True)
    subject = models.CharField(max_length=100)
    comment = models.TextField(null=True)
    created_on = models.DateTimeField(auto_now_add = True)

class BusinessCoupons(models.Model):
    title = models.CharField(max_length=150)
    business = models.ForeignKey("Business",related_name='buz_coupon')
    photo = ThumbnailerImageField(upload_to=get_bizgallery_path,resize_source=dict(size=(700, 0), crop='smart'), null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    description = models.CharField(max_length=2000)
    is_active=models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='couponcreatedby',null=True)
    created_on = models.DateTimeField('couponCreatedon',auto_now_add=True)
    type=models.CharField(max_length=1,choices=COUPON_OFFER_TYPE)

    def __unicode__(self):
        return self.title
    def get_delete_url(self):
        return reverse('business_delete_coupon_photo', args=[self.id])
    def get_absolute_url(self):
        return self.business.get_absolute_url()+'?view=coupons&cid=%s'%(self.id)

class BusinessProducts(models.Model):
    title = models.CharField(max_length=150)
    business = models.ForeignKey("Business",related_name='buz_product')
    photo = ThumbnailerImageField(upload_to=get_bizgallery_path,resize_source=dict(size=(700, 0), crop='smart'), null=True)
    description = models.CharField(max_length=1000,null=True)
    price = models.CharField(max_length=50,null=True)
    is_active=models.BooleanField(default=False)
    created_by = models.ForeignKey(User,related_name='productcreatedby',null=True)
    created_on = models.DateTimeField('productCreatedon',auto_now_add=True)

    def __unicode__(self):
        return self.title

    def get_delete_url(self):
        return reverse('business_delete_product_photo', args=[self.id])

    def get_absolute_url(self):
        return self.business.get_absolute_url()+'?view=products&pid=%s'%(self.id)

class BusinessPrice(models.Model):
    level = models.CharField(max_length=10,null=True)
    level_visibility = models.BooleanField(default=True)
    level_label = models.CharField(max_length=50,null=True)
    is_paid = models.BooleanField(default=True)
    exposure = models.CharField(max_length=2,null=True)
    images = models.CharField(max_length=1,null=True)#Y=Yes N=No E=None
    offer_coupon = models.CharField(max_length=1,null=True)#Y=Yes N=No E=None
    product = models.CharField(max_length=1,null=True)#Y=Yes N=No E=None
    share_buttons = models.CharField(max_length=1,null=True)#Y=Yes N=No E=None
    comments = models.CharField(max_length=1,null=True)#Y=Yes N=No E=None
    newsletter = models.CharField(max_length=1,null=True)#Y=Yes N=No E=None
    socialmedia = models.CharField(max_length=1)
    price_month = models.FloatField(default=0.0)
    price_year = models.FloatField(default=0.0)

    def get_exposure(self):
        if self.exposure=='1':return _('5X')
        elif self.exposure=='2':return _('10X')
        elif self.exposure=='3':return _('15X')
        elif self.exposure=='4':return _('20X')
        elif self.exposure=='5':return _('25X')
        else:return _('Standard')
#Business_Exposure=(('0','Standard'),('1',' 5X'),('2','10X'),('3','15X'),('4','20X'),('5','25X'),)

class BusinessClaimSettings(models.Model):
    allow_claim                 = models.BooleanField(default=False)
    allow_free_buz_claim        = models.BooleanField(default=False)
    auto_aprove_free_buz_claim  = models.BooleanField(default=False)
    auto_aprove_paid_buz_claim  = models.BooleanField(default=False)
    after_failed_payment = models.CharField(max_length=1,default='F',null=True,blank=True)#F BASIC B Blocked

    @classmethod
    def get_setting(cls):
        try:return BusinessClaimSettings.objects.all()[:1][0]
        except:return False

class BusinessClaim(models.Model):
    business        = models.ForeignKey("Business",related_name='buz_claim')
    staff           = models.ForeignKey(User,related_name='buz_claim_staff')
    user            = models.ForeignKey(User,related_name='buz_claim_user')
    is_approved     = models.BooleanField(default=False)
    is_paid         = models.BooleanField(default=False)
    claimed_on      = models.DateTimeField('buz_claimed_on',auto_now_add=True)
    approved_on     = models.DateTimeField('buz_approved_on',null=True,blank=True)
    payment_status  = models.CharField(max_length=1,null=True)#B=Free S=Sponsored F=Featured


