import os
import uuid

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from easy_thumbnails.fields import ThumbnailerImageField
from common.utils import get_global_settings
from mptt.models import MPTTModel,TreeForeignKey
from common.models import Basetable
from bmshop.products.settings import DELIVERY_TIME_UNIT_CHOICES,DELIVERY_TIME_UNIT_DAYS
from bmshop.products.settings import PROPERTY_FIELD_CHOICES,PROPERTY_TEXT_FIELD,PROPERTY_SELECT_FIELD,PROPERTY_NUMBER_FIELD
from bmshop.shop.models import Shop

from django.conf import settings
User = settings.AUTH_USER_MODEL

TAX_OPTION = [
    ['PIT', _(u'Price Includes Tax')],
    ['PET', _(u'Price Excludes Tax')],
]

TAX_OPTION_DESC = {
    'PIT': _(u'Price Includes Tax'),
    'PET': _(u'Price Excludes Tax')
}

def get_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('eshop/images', filename)


class Category(MPTTModel):
    name = models.CharField( max_length=50)
    slug = models.SlugField(unique=True)
    parent =TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    show_all_products = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    position = models.IntegerField(default=0)
    
    meta_title = models.CharField(max_length=100,blank=True)
    meta_description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        global_settings = get_global_settings()
        url = reverse('bmshop_product_home') + self.slug + '/'
        return url
    
    def get_subcat_url(self):
        global_settings = get_global_settings()
        url = reverse('bmshop_product_home') +self.get_root().slug+'/'+ self.slug + '/'
        return url
    
    def get_all_children(self):

        def _get_all_children(category, children):
            for category in Category.objects.filter(parent=category.id):
                children.append(category)
                _get_all_children(category, children)

        children = []
        for category in Category.objects.filter(parent=self.id):
            children.append(category)
            _get_all_children(category, children)
        return children
    
    def get_children(self):
        return Category.objects.filter(parent=self.id).order_by('position')
    
    def get_featued_children(self):
        return Category.objects.filter(parent=self.id,featured=True).order_by('position')
    
    def get_featured_products_home(self):
        cat_ids = []
        product_objs = None
        if self.get_all_children():
            product_objs = Product.objects.filter(categories__in=self.get_all_children(),featured=True,status="P")[:4]  
        return product_objs     
    
    def get_featured_products_catlist(self):
        if self.get_all_children():
            product_objs = Product.objects.filter(categories__in=self.get_all_children(),status="P").order_by('-featured')[:4]  
        else:
            product_objs = self.products.filter(status="P").order_by('-featured')[:4]
        return product_objs    
          
    def get_parent(self):
        parent = self.parent
        return parent
    
    def get_parents(self):
        parents = []
        category = self.parent
        while category is not None:
            parents.append(category)
            category = category.parent
        parents.reverse()
        return parents    
    
    def get_product_count(self):
        count = Product.objects.filter(categories=self.id).count()
        return count
    
    
class Product(Basetable):
    
    name = models.CharField(help_text=_(u"The name of the product."), max_length=120, blank=True)
    slug = models.SlugField(unique=True, max_length=120)
    uid = models.CharField(help_text=_(u"Unique number of the product."), blank=True, max_length=30)
    categories = models.ManyToManyField("Category", verbose_name=_(u"Products"), blank=True, related_name="products")
    
    price = models.FloatField(default=0.0)
    tax_calculator = models.CharField(null=True, blank=True,choices=TAX_OPTION,max_length=255)
    static_price = models.CharField(max_length=10,blank=True)
    
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    meta_title = models.CharField(blank=True, max_length=120)
    meta_description = models.TextField(blank=True)
    
    related_products = models.ManyToManyField("self", verbose_name=_(u"Related products"), blank=True, null=True,
        symmetrical=False, related_name="bm_related_products")
    accessories = models.ManyToManyField("self", verbose_name=_(u"Acessories"), blank=True, null=True,
        symmetrical=False, through="BMPAccessories",related_name="reverse_accessories")
    
    for_sale = models.BooleanField(default=False)
    for_sale_price = models.FloatField(default=0.0,blank=True, null=True)
    rating = models.FloatField(default=0)
    
    deliverable = models.BooleanField(default=True)
    manual_delivery_time = models.BooleanField( default=False)
    delivery_time = models.ForeignKey("DeliveryTime", verbose_name=_(u"Delivery time"), blank=True, null=True, related_name="products_delivery_time",on_delete=models.SET_NULL)
    manage_stock_amount = models.BooleanField(default=False)
    stock_amount = models.CharField(max_length=10)
    
    manufacturer = models.ForeignKey("Manufacturer", verbose_name=_(u"Manufacturer"), blank=True, null=True, related_name="products",on_delete=models.SET_NULL)
    most_viewed = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name
    
    def get_tax_calculator(self):
        try:return TAX_OPTION_DESC[self.tax_calculator]
        except:return ''
        
    def get_absolute_url(self):
        global_settings = get_global_settings()
        url = reverse('bmshop_product_home') + self.slug + '.html'
        return url

    def get_default_photo(self):
        try:
            photo = self.product_photos.filter(product=self.id,default=True)[:1][0]
            return photo.id
        except:
            return None
    
    def get_cover_image_staff(self):
        try:
            photo = self.product_photos.filter(product=self.id,default=True)[:1][0]
            return photo.photo
        except:
            photos = self.product_photos.filter(product=self)[:1]
            if photos:
                for photo in photos:
                    return photo.photo
            else:
                return False    
    
    def get_default_image_staff(self):
        return settings.STATIC_URL+"ui/images/global/img-none.png"    
    
    def get_cover_image_user(self):
        try:
            photo = self.product_photos.filter(product=self.id,default=True)[:1][0]
            return photo.photo
        except:
            photos = self.product_photos.filter(product=self)[:1]
            if photos:
                for photo in photos:
                    return photo.photo
            else:
                return False          
    
    def get_all_photos(self):

        return self.product_photos.filter(product=self.id)
    
    def get_accessories(self):
        acc_ids = []
        acc_objs = self.productaccessories_product.filter(accessory__status='P')
        for acc in acc_objs:
            acc_ids.append(acc.accessory.id)
        
        return acc_ids
    
    def get_base_price(self):
        if self.price == self.for_sale_price:
            return None
        elif self.price > self.for_sale_price:
            return self.price
        else:
            return None
    
    def get_tax(self):
        """
        Tax Amount
        """
        if self.tax_calculator == 'PET':
            shop_obj = Shop.get_shop_settings()
            if shop_obj.is_taxes:
                rate = shop_obj.tax_value
                return self.for_sale_price * (rate / (rate + 100))
            else:
                return 0
        else:
            return 0
    
    def get_tax_rate(self):
        """
        Product Price with TAax Amount
        """
        if self.tax_calculator == 'PET':
            shop_obj = Shop.get_shop_settings()
            if shop_obj.is_taxes:
                rate = shop_obj.tax_value
                price = self.for_sale_price * ((100 + rate) / 100)
                return price
            else:
                return self.for_sale_price
        else:
            return self.for_sale_price
    
    def get_product_stock(self):
        if self.manage_stock_amount:
            if self.stock_amount <= 0:
                return False
            else:
                return True    
        else:
            return True
    
    def decrease_stock_amount(self, amount):
        if self.manage_stock_amount:
            stk_amnt = float(self.stock_amount)
            stk_amnt -= int(amount)
        self.save()

    
    def get_global_properties(self):
        properties = []
        for property_group in self.property_groups.all():
            properties.extend(property_group.properties.order_by("bmgroupsproperties"))

        return properties

    def get_local_properties(self):
        return self.properties.order_by("bmproductsproperties")
    
    def get_properties(self):
        properties = self.get_global_properties()

        properties.extend(self.get_local_properties())

        properties.sort(lambda a, b: cmp(a.position, b.position))

        return properties
    
    def get_delivery_time(self):
        if self.manual_delivery_time:
            return "%s - %s %s"%(self.delivery_time.min_unit,
                self.delivery_time.max_unit,self.delivery_time.get_unit_display())
        else:
            return None
    
    def get_manufacture(self):
        
        return self.manufacturer.name
    
    def get_category(self):
        return self.categories.all()[:1]
    
    def get_categories(self):
        categories = self.categories.all()
        return categories
        
class BMPAccessories(models.Model):
    product = models.ForeignKey("Product",verbose_name=_(u"Product"), related_name="productaccessories_product")
    accessory = models.ForeignKey("Product",verbose_name=_(u"Accessory"), related_name="productaccessories_accessory")
    quantity = models.FloatField(default=1)    
    
    def __unicode__(self):
        return "%s -> %s" % (self.product.name, self.accessory.name)
    
class BMPropertyGroup(Basetable):
    name = models.CharField(_(u"Name"), blank=True, max_length=50)
    products = models.ManyToManyField("Product", verbose_name=_(u"Products"), related_name="property_groups")  
    position = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name
    
    def get_property_group(self):
        return BMGroupsProperties.objects.filter(group=self.id)
    
    def get_filterable_properties(self):
        return self.properties.filter(filterable=True)
    
    def get_displayble_properties(self):
        return self.properties.filter(display_on_product=True)
       
    
class BMProperty(Basetable):    
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    groups = models.ManyToManyField("BMPropertyGroup", verbose_name=_(u"Group"), blank=True, null=True, through="BMGroupsProperties", related_name="properties")
    products = models.ManyToManyField("Product", verbose_name=_(u"Products"), blank=True, null=True, through="BMProductsProperties", related_name="properties")
    position = models.IntegerField(default=0)
    type = models.PositiveSmallIntegerField(choices=PROPERTY_FIELD_CHOICES, default=PROPERTY_TEXT_FIELD)
    short_description = models.TextField(blank=True)
    display_on_product = models.BooleanField(default=True)
    filterable = models.BooleanField(default=True)
    display_no_results = models.BooleanField(default=False)
    
    add_price = models.BooleanField(_(u"Add price"), default=True)
    
    def __unicode__(self):
        return self.name
    
    def is_select_field(self):
        return self.type == PROPERTY_SELECT_FIELD

    def is_text_field(self):
        return self.type == PROPERTY_TEXT_FIELD
    
    def is_number_field(self):
        return self.type == PROPERTY_NUMBER_FIELD
    
    def get_property_option(self):
        return PropertyOption.objects.filter(property=self.id).order_by('name')
    
    def is_valid_value(self, value):
        if self.is_number_field():
            try:
                float(value)
            except ValueError:
                return False
        return True
    
    
class BMGroupsProperties(models.Model):
    group = models.ForeignKey("BMPropertyGroup", verbose_name=_(u"Group"), related_name="groupproperties")
    property = models.ForeignKey("BMProperty", verbose_name=_(u"BMProperty"))
    position = models.IntegerField(default=0)

    class Meta:
        ordering = ("position", )
        unique_together = ("group", "property")  
    
class BMProductsProperties(models.Model):
    product = models.ForeignKey("Product", verbose_name=_(u"Product"), related_name="productsproperties")
    property = models.ForeignKey("BMProperty", verbose_name=_(u"BMProperty"))
    
    class Meta:
        unique_together = ("product", "property")
    
            
class PropertyOption(models.Model):    
    property = models.ForeignKey("BMProperty", verbose_name=_(u"Property"), related_name="options")
    name = models.CharField(max_length=100)
    price = models.FloatField(blank=True, null=True, default=0.0)
    short_description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name    
    
class ProductPropertyValue(models.Model):
    product = models.ForeignKey("Product", verbose_name=_(u"Product"), related_name="property_values")
    property = models.ForeignKey("BMProperty", verbose_name=_(u"Property"), related_name="property_values")
    group = models.ForeignKey("BMPropertyGroup", verbose_name=_(u"Group"), related_name="group_values")
    value = models.CharField(blank=True, max_length=100)
    value_as_float = models.FloatField(blank=True, null=True)
    type = models.PositiveSmallIntegerField()    
    
    class Meta:
        unique_together = ("product", "property", "value", "type")

    def __unicode__(self):
        return self.value
    
    def save(self, *args, **kwargs):
        try:
            float(self.value)
        except ValueError:
            pass
        else:
            self.value_as_float = self.value

        super(ProductPropertyValue, self).save(*args, **kwargs)

    
    
class ProductPhoto(models.Model):    
    product = models.ForeignKey("Product",null=True,related_name="product_photos")
    title = models.CharField(max_length=200, null=True)
    default = models.BooleanField(default=False)
    photo = ThumbnailerImageField(upload_to=get_image_path, resize_source=dict(size=(700, 0), crop='smart'),)
    uploaded_on = models.DateTimeField('createdonproductphoto', auto_now_add=True)
    uploaded_by = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.title
    
    def get_delete_url(self):
        return reverse('staff_bmshop_ajax_delete_photos', args=[self.id])
    
class DeliveryTime(models.Model):
    min_unit = models.CharField(max_length=10)
    max_unit = models.CharField(max_length=10)
    unit = models.PositiveSmallIntegerField(_(u"Unit"), choices=DELIVERY_TIME_UNIT_CHOICES, default=DELIVERY_TIME_UNIT_DAYS)
    description = models.TextField(_(u"Description"), blank=True)

    def __unicode__(self):
        return '%s - %s %s'%(self.min_unit,self.max_unit,self.get_unit_display())

class Manufacturer(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField( unique=True, max_length=80)
    categories = models.ManyToManyField("Category", verbose_name=_(u"Manufactures"), blank=True, related_name="manufactures")
    
    def __unicode__(self):
        return self.name    
    
    
    
            
    
    
    
    
    
    
    
    
    
    
    