from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from bmshop.products.models import Product,BMProperty,PropertyOption
from bmshop.shop.models import Shop,Shipping
User = settings.AUTH_USER_MODEL

class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u"User"), blank=True, null=True)
    session = models.CharField(_(u"Session"), blank=True, max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    def __unicode__(self):
        return u"%s, %s" % (self.user, self.session)
    
    def get_cart_items(self):
        items = CartItem.objects.filter(cart=self, product__status="P").order_by("-id")
        return items
    
    def add(self, product, amount ,properties=None):
        cart_item=None
        total_amount = 0
        added = False
        for item in CartItem.objects.filter(cart=self, product=product):
            total_amount += item.amount
        
        if properties:
            for item in CartItem.objects.filter(cart=self, product=product):
                item_props = {}
                if item.get_properties():
                    for pv in item.properties.all():
                        item_props[pv.property.id] = pv.value

                    shared_item = set(item_props.items()) & set(properties.items())
                    item_len = len(item_props)
                    comp_len = len(shared_item)
                    prop_len = len(properties)
                    if item_len == comp_len:
                        if item_len == comp_len:
                            cart_item = item
                            break
                        else:
                            cart_item = None
        else:
            for item in CartItem.objects.filter(cart=self, product=product):
                cart_item = item

        if cart_item:
            total_amounts=total_amount+amount
            if product.manage_stock_amount:
                if total_amounts > float(product.stock_amount):
                    amount = float(product.stock_amount)-total_amount
                    msg ="Sorry there are only "+str(product.stock_amount)+" stock of "+product.name+" available"
                    added = False
                    cart_item.amount += amount
                    cart_item.save()
                else:
                    cart_item.amount += amount
                    if cart_item.amount > float(product.stock_amount):
                        cart_item.amount = float(product.stock_amount)
                        msg ="Sorry there are only "+str(product.stock_amount)+" stock of "+product.name+" available"
                        added = False
                    else:
                        cart_item.amount = cart_item.amount
                        msg = product.name+" is updated to your shopping bag "
                        added = True
            else:
                msg = product.name+" is updated to your shopping bag "
                added = True
                cart_item.amount += amount
            cart_item.save()
        else:
            total_amounts=total_amount+amount
            if product.manage_stock_amount:
                if total_amounts > float(product.stock_amount):
                    amount = float(product.stock_amount)-total_amount
                    if amount < 1:
                        amount = 0
            
            cart_item = CartItem.objects.create(cart = self, product = product, amount = amount)
            if properties:
                for property_id, value in properties.items():
                    try:
                        Property.objects.get(pk=property_id)
                    except Property.DoesNotExist:
                        pass
                    else:
                        CartItemPropertyValue.objects.create(cart_item=cart_item, property_id=property_id, value=value)
                msg = product.name+" is added to your shopping bag "
                added = True
            else:
                
                msg = product.name+" is added to your shopping bag "
                added = True
            if cart_item.amount < 1:
                cart_item.delete()
                msg = "Sorry "+product.name+" is out of stock"
                added = False

        return cart_item,msg,added
    
    def add_update(self, product, amount ,properties=None):
        cart_item=None
        total_amount = amount
        added = False
        
        if properties:
            for item in CartItem.objects.filter(cart=self, product=product):
                item_props = {}
                if item.get_properties():
                    for pv in item.properties.all():
                        item_props[pv.property.id] = pv.value

                    shared_item = set(item_props.items()) & set(properties.items())
                    item_len = len(item_props)
                    comp_len = len(shared_item)
                    prop_len = len(properties)
                    if item_len == comp_len:
                        if item_len == comp_len:
                            cart_item = item
                            break
                        else:
                            cart_item = None
        else:
            for item in CartItem.objects.filter(cart=self, product=product):
                cart_item = item

        if cart_item:
            total_amounts=amount
            if product.manage_stock_amount:
                if total_amounts > float(product.stock_amount):
                    amount = float(product.stock_amount)-total_amount
                    msg ="Sorry there are only "+str(product.stock_amount)+" stock of "+product.name+" available"
                    added = False
                    cart_item.amount = int(product.stock_amount)
                    cart_item.save()
                    total_amount=product.stock_amount
                else:
                    cart_item.amount = amount
                    if cart_item.amount > float(product.stock_amount):
                        cart_item.amount = product.stock_amount
                        total_amount=product.stock_amount
                        msg ="Sorry there are only "+str(product.stock_amount)+" stock of "+product.name+" available"
                        added = False
                        cart_item.save()
                    else:
                        cart_item.amount = cart_item.amount
                        msg = product.name+" is updated to your shopping bag "
                        added = True
                        cart_item.save()
            else:
                msg = product.name+" is updated to your shopping bag "
                added = True
                cart_item.amount = amount
            cart_item.save()
        else:
            total_amounts=amount
            if product.manage_stock_amount:
                if total_amounts > float(product.stock_amount):
                    amount = float(product.stock_amount)-total_amount
                    if amount < 1:
                        amount = 0
            
            cart_item = CartItem.objects.create(cart = self, product = product, amount = amount)
            if properties:
                for property_id, value in properties.items():
                    try:
                        Property.objects.get(pk=property_id)
                    except Property.DoesNotExist:
                        pass
                    else:
                        CartItemPropertyValue.objects.create(cart_item=cart_item, property_id=property_id, value=value)
                msg = product.name+" is added to your shopping bag "
                added = True
            else:
                
                msg = product.name+" is added to your shopping bag "
                added = True
            if cart_item.amount < 1:
                cart_item.delete()
                msg = "Sorry "+product.name+" is out of stock"
                added = False
            cart_item.amount=total_amounts
        cart_item.save()
        return cart_item,msg,added
    
    def validate_cart(self):
        msgs = []
        for item in self.get_cart_items():
            if item.product.manage_stock_amount:
                 if float(item.amount) > float(item.product.stock_amount):
                     msg ="Sorry there are only "+str(item.product.stock_amount)+" stock of "+item.product.name+" available"
                     item.amount = float(item.product.stock_amount)
                     item.save()
                     msgs.append(msg)
        return msgs        
                
    def get_total_items(self):
        amount = 0
        cart_items = self.get_cart_items()
        for item in cart_items:
            amount += int(item.amount)
        return amount
    
    def get_price(self):
        price = 0
        for item in self.get_cart_items():
            price += item.get_product_total_price()
        return price
    
    def get_total_tax(self):
        amount = 0
        tax = 0
        shop_obj = Shop.get_shop_settings()
        
        if shop_obj.is_taxes:
            for item in self.get_cart_items():
                if item.is_tax_rate():
                    amount += item.get_product_total_price()
                    
            rate = shop_obj.tax_value
            tax = amount * (rate / (rate + 100))    
        
        return tax
    
    def get_shipping_method(self):
        try:
            ship_obj = Shipping.get_shippment_settings()
            return ship_obj.name
        except:
            return None 
    
    def get_shipping_charge(self):
        try:
            ship_obj = Shipping.get_shippment_settings()
            return ship_obj.price
        except:
            return 0  
        
    def get_total_price(self):
        price = self.get_price() + self.get_total_tax()
        try:
            ship_obj = Shipping.get_shippment_settings()
            price+=ship_obj.price
        except:
            pass    
        return price
    
    
class CartItem(models.Model):
    cart = models.ForeignKey("Cart", verbose_name=_(u"Cart"))
    product = models.ForeignKey(Product, verbose_name=_(u"Product"))
    amount = models.FloatField(max_length=10, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True, auto_now_add=True)  
    
    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return "cart_item_%s_%s"%(self.cart,self.product)
    
    def get_product_total_price(self):
        price = self.product.for_sale_price * self.amount
        return price
    
    def is_tax_rate(self):
        if self.product.tax_calculator == 'PET':
            return True
        else:return False
    
    def get_properties(self):
        properties = []
        for property in self.product.get_properties():
            try:
                cipv = CartItemPropertyValue.objects.get(cart_item=self, property=property)
            except CartItemPropertyValue.DoesNotExist:
                continue

            if property.is_select_field:
                try:
                    option = PropertyOption.objects.get(pk=int(cipv.value))
                except (PropertyOption.DoesNotExist, ValueError):
                    value = cipv.value
                else:
                    value = option.name
            else:
                value = cipv.value

            properties.append({
                "name": property.name,
                "title": property.title,
                "value": value,
                "obj": property
            })
        return properties
    
class CartItemPropertyValue(models.Model):
    cart_item = models.ForeignKey("CartItem", verbose_name=_(u"Cart item"), related_name="cart_properties")
    property = models.ForeignKey(BMProperty, verbose_name=_(u"Property"))
    value = models.CharField("Value", blank=True, max_length=100)  
    
    def __unicode__(self):
        return "cart_item_value%s_%s"%(self.property,self.value)  
    
    
    
    
    
    
    
    
    