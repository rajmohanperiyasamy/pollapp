from  xml.etree.ElementTree import fromstring
import pycurl
import cStringIO

from payments.googlecheckout.models import GCNewOrderNotification
from django.conf import settings
from xml.dom.minidom import Document
import hmac, hashlib, base64
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.conf.urls import patterns
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from common.utils import *
from django.dispatch import Signal
from common.models import PaymentConfigure

transaction_started = Signal()

transaction_was_successful = Signal(providing_args=["type", "response"])
transaction_was_unsuccessful = Signal(providing_args=["type", "response"])
transactionnotification_was_successful = Signal(providing_args=["type", "response"])
csrf_exempt_m = method_decorator(csrf_exempt)
require_POST_m = method_decorator(require_POST)

PROD_URL = 'https://sandbox.google.com/checkout/api/checkout/v2/checkout/Merchant/%s' 
#PROD_URL = 'https://checkout.google.com/api/checkout/v2/checkout/Merchant/%s'
BUTTON_URL = 'http://sandbox.google.com/checkout/buttons/checkout.gif?merchant_id=%(merchant_id)s&w=%(width)s&h=%(height)s&style=white&variant=text&loc=en_US'
#BUTTON_URL = 'http://checkout.google.com/checkout/buttons/checkout.gif?merchant_id=%(merchant_id)s&w=%(width)s&h=%(height)s&style=white&variant=text&loc=en_US'


class GoogleCheckoutIntegration(object):
    def __init__(self, options=None):
        self.fields = {}
        self.merchant_id=options['merchant_id']
        self.merchant_key=options['merchant_key']
        if not options:options = {}
        self._signature = None
       
    def add_field(self, key, value):
        self.fields[key] = value

    def add_fields(self, params):
        for (key, val) in params.iteritems():
            self.add_field(key, val)
            
    @property
    def service_url(self):
        return PROD_URL % self.merchant_id

    def button_image_url(self):
        params = {"merchant_id": self.merchant_id, 
                  "width": self.button_width,
                  "height": self.button_height}
        return BUTTON_URL % params

    @property
    def button_width(self):
        return self.fields.get("button_width", 180)

    @property
    def button_height(self):
        return self.fields.get("button_height", 46)
    
    def subs_generate_cart_xml(self):
        doc = Document()
        root = doc.createElement('checkout-shopping-cart')
        root.setAttribute('xmlns', 'http://checkout.google.com/schema/2')
        doc.appendChild(root)
        cart = doc.createElement('shopping-cart')
        root.appendChild(cart)
        items = doc.createElement('items')
        cart.appendChild(items)

        ip_items = self.fields.get("items", [])
        for item in ip_items:
            it = doc.createElement("item")
            items.appendChild(it)
            it_name = doc.createElement("item-name")
            it_name.appendChild(doc.createTextNode(unicode(item["name"])))
            it.appendChild(it_name)
            it_descr = doc.createElement('item-description')
            it_descr.appendChild(doc.createTextNode(unicode(item["description"])))
            it.appendChild(it_descr)
            it_price = doc.createElement("unit-price")
            it_price.setAttribute("currency", unicode(item["currency"]))
            it_price.appendChild(doc.createTextNode(unicode(item["amount"])))
            it.appendChild(it_price)
            it_qty = doc.createElement("quantity")
            it_qty.appendChild(doc.createTextNode(unicode(item["quantity"])))
            it.appendChild(it_qty)
            
            it_unique_id = doc.createElement("merchant-item-id")
            it_unique_id.appendChild(doc.createTextNode(unicode(item["id"])))
            it.appendChild(it_unique_id)
            
            merchant_private_item_data= doc.createElement("merchant-private-item-data")
            merchant_private_item_data.appendChild(doc.createTextNode(unicode(item["id"])))
            it.appendChild(merchant_private_item_data)
            
            sub=doc.createElement("subscription")
            sub.setAttribute('type', 'google')
            sub.setAttribute('period',unicode(item["listing_period"]))
            it.appendChild(sub)
            
            sub_payment = doc.createElement("payments")
            sub.appendChild(sub_payment)
            
            sub_payment_subscription = doc.createElement("subscription-payment")
            #sub_payment_subscription.setAttribute('times','2')
            sub_payment.appendChild(sub_payment_subscription)
             
            sub_payment_subscription_payment = doc.createElement("maximum-charge")
            sub_payment_subscription_payment.setAttribute('currency',unicode(item["currency"]))
            sub_payment_subscription_payment.appendChild(doc.createTextNode(unicode(item["amount"])))
            sub_payment_subscription.appendChild(sub_payment_subscription_payment)
            
            
            recurrent = doc.createElement("recurrent-item")
            sub.appendChild(recurrent)
            
            
            it_names = doc.createElement("item-name")
            it_names.appendChild(doc.createTextNode(unicode(item["name"])))
            it_descrs = doc.createElement('item-description')
            it_descrs.appendChild(doc.createTextNode(unicode(item["description"])))
            it_prices = doc.createElement("unit-price")
            it_prices.setAttribute("currency", unicode(item["currency"]))
            it_prices.appendChild(doc.createTextNode(unicode(item["amount"])))
            it_qtys = doc.createElement("quantity")
            it_qtys.appendChild(doc.createTextNode(unicode(item["quantity"])))
            
            
            recurrent.appendChild(it_names)
            recurrent.appendChild(it_descrs)
            recurrent.appendChild(it_qtys)
            recurrent.appendChild(it_prices)
            
            digital_content = doc.createElement("digital-content")
            recurrent.appendChild(digital_content)
            
            display_disposition = doc.createElement("display-disposition")
            display_disposition.appendChild(doc.createTextNode(unicode('OPTIMISTIC')))
            digital_content.appendChild(display_disposition)
            
            #url = doc.createElement("url")
            #url.appendChild(doc.createTextNode(unicode('http://mywebsite.example.com')))
            #digital_content.appendChild(url)
            
            description = doc.createElement("description")
            description.appendChild(doc.createTextNode(unicode(item["description"])))
            digital_content.appendChild(description)
        
        checkout_flow = doc.createElement('checkout-flow-support')
        root.appendChild(checkout_flow)
        merchant_checkout_flow = doc.createElement('merchant-checkout-flow-support')
        checkout_flow.appendChild(checkout_flow)
        return_url = doc.createElement('continue-shopping-url')
        return_url.appendChild(doc.createTextNode(self.fields["return_url"]))
        merchant_checkout_flow.appendChild(return_url)

        cart_xml = doc.toxml(encoding="utf-8")
        hmac_signature = hmac.new(self.merchant_key,cart_xml,hashlib.sha1).digest()
        self._signature = base64.b64encode(hmac_signature)
        return base64.b64encode(cart_xml)
    
    def generate_cart_xml(self):
        doc = Document()
        root = doc.createElement('checkout-shopping-cart')
        root.setAttribute('xmlns', 'http://checkout.google.com/schema/2')
        doc.appendChild(root)
        cart = doc.createElement('shopping-cart')
        root.appendChild(cart)
        items = doc.createElement('items')
        cart.appendChild(items)
        ip_items = self.fields.get("items", [])
        for item in ip_items:
            it = doc.createElement("item")
            items.appendChild(it)
            it_name = doc.createElement("item-name")
            it_name.appendChild(doc.createTextNode(unicode(item["name"])))
            it.appendChild(it_name)
            it_descr = doc.createElement('item-description')
            it_descr.appendChild(doc.createTextNode(unicode(item["description"])))
            it.appendChild(it_descr)
            it_price = doc.createElement("unit-price")
            it_price.setAttribute("currency", unicode(item["currency"]))
            it_price.appendChild(doc.createTextNode(unicode(item["amount"])))
            it.appendChild(it_price)
            it_qty = doc.createElement("quantity")
            it_qty.appendChild(doc.createTextNode(unicode(item["quantity"])))
            it.appendChild(it_qty)
            it_unique_id = doc.createElement("merchant-item-id")
            it_unique_id.appendChild(doc.createTextNode(unicode(item["id"])))
            it.appendChild(it_unique_id)
        checkout_flow = doc.createElement('checkout-flow-support')
        root.appendChild(checkout_flow)
        merchant_checkout_flow = doc.createElement('merchant-checkout-flow-support')
        checkout_flow.appendChild(merchant_checkout_flow)
        return_url = doc.createElement('continue-shopping-url')
        return_url.appendChild(doc.createTextNode(self.fields["return_url"]))
        merchant_checkout_flow.appendChild(return_url)
        cart_xml = doc.toxml(encoding="utf-8")
        
        hmac_signature = hmac.new(self.merchant_key,cart_xml,hashlib.sha1).digest()
        self._signature = base64.b64encode(hmac_signature)
        return base64.b64encode(cart_xml)

    def signature(self):
        if not self._signature:
            self.generate_cart_xml()
        return self._signature

    def gc_cart_items_blob(self, post_data):
        items = post_data.getlist('shopping-cart.items')
        cart_blob = ''
        for item in items:
            item_id = post_data.get('%s.merchant-item-id' % (item), '')
            item_name = post_data.get('%s.item-name' % (item), '')
            item_desc = post_data.get('%s.item-description' % (item), '')
            item_price = post_data.get('%s.unit-price' % (item), '')
            item_price_currency = post_data.get('%s.unit-price.currency' % (item), '')
            item_quantity = post_data.get('%s.quantity' % (item), '')
            cart_blob += '%(item_id)s\t%(item_name)s\t%(item_desc)s\t%(item_price)s\t%(item_price_currency)s\t%(item_quantity)s\n\n' % ({"item_id": item_id,
                                                                                                                                         "item_name": item_name,
                                                                                                                                         "item_desc": item_desc,
                                                                                                                                         "item_price": item_price,
                                                                                                                                         "item_price_currency": item_price_currency,
                                                                                                                                         "item_quantity": item_quantity,})
        return cart_blob
    
    def custom_gc_cart_items_blob(self, post_data,namespace):
        items = post_data.findall(".//{%s}shopping-cart/.//{%s}items"  % (namespace,namespace))
        cart_blob = ''
        for item in items:
            item_id = post_data.findtext('.//{%s}shopping-cart/.//{%s}items/.//{%s}merchant-item-id' % (namespace,namespace,namespace))
            item_name = post_data.findtext('.//{%s}shopping-cart/.//{%s}items/.//{%s}item-name' % (namespace,namespace,namespace))
            item_desc = post_data.findtext('.//{%s}shopping-cart/.//{%s}items/.//{%s}item-description' % (namespace,namespace,namespace))
            item_price = post_data.findtext('.//{%s}shopping-cart/.//{%s}items/.//{%s}unit-price' % (namespace,namespace,namespace))
            item_price_currency = post_data.find('.//{%s}shopping-cart/.//{%s}items/.//{%s}unit-price' % (namespace,namespace,namespace)).attrib['currency']
            item_quantity = post_data.findtext('.//{%s}shopping-cart/.//{%s}items/.//{%s}quantity' % (namespace,namespace,namespace))
            cart_blob += '%(item_id)s#@#%(item_name)s#@#%(item_desc)s#@#%(item_price)s\t%(item_price_currency)s\t%(item_quantity)s\n\n' % ({"item_id": item_id,
                                                                                                                                         "item_name": item_name,
                                                                                                                                         "item_desc": item_desc,
                                                                                                                                         "item_price": item_price,
                                                                                                                                         "item_price_currency": item_price_currency,
                                                                                                                                         "item_quantity": item_quantity,})
        return cart_blob

    
    def gc_new_order_notification(self, request):
        post_data = request.POST.copy()
        data = {}

        resp_fields = {
            "_type": "notify_type",
            "serial-number" : "serial_number",      
            "google-order-number" : "google_order_number",
            "buyer-id" : "buyer_id",           
            "buyer-shipping-address.contact-name" : "shipping_contact_name",
            "buyer-shipping-address.address1" : "shipping_address1",    
            "buyer-shipping-address.address2" : "shipping_address2",    
            "buyer-shipping-address.city" : "shipping_city",        
            "buyer-shipping-address.postal-code" : "shipping_postal_code", 
            "buyer-shipping-address.region" : "shipping_region",      
            "buyer-shipping-address.country-code" : "shipping_country_code",
            "buyer-shipping-address.email" : "shipping_email",       
            "buyer-shipping-address.company-name" : "shipping_company_name",
            "buyer-shipping-address.fax" : "shipping_fax",         
            "buyer-shipping-address.phone" : "shipping_phone",       
            "buyer-billing-address.contact-name" : "billing_contact_name",
            "buyer-billing-address.address1" : "billing_address1",    
            "buyer-billing-address.address2" : "billing_address2",    
            "buyer-billing-address.city" : "billing_city",        
            "buyer-billing-address.postal-code" : "billing_postal_code", 
            "buyer-billing-address.region" : "billing_region",      
            "buyer-billing-address.country-code" : "billing_country_code",
            "buyer-billing-address.email" : "billing_email",       
            "buyer-billing-address.company-name" : "billing_company_name",
            "buyer-billing-address.fax" : "billing_fax",         
            "buyer-billing-address.phone" : "billing_phone",       
            "buyer-marketing-preferences.email-allowed" : "marketing_email_allowed",
            "order-adjustment.total-tax" : "total_tax",                
            "order-adjustment.total-tax.currency" : "total_tax_currency",       
            "order-adjustment.adjustment-total" : "adjustment_total",         
            "order-adjustment.adjustment-total.currency" : "adjustment_total_currency",
            "order-total" : "order_total",
            "order-total.currency" : "order_total_currency",
            "financial-order-state" : "financial_order_state",  
            "fulfillment-order-state" : "fulfillment_order_state",
            "timestamp" : "timestamp",
            }
        
        for (key, val) in resp_fields.iteritems():
            data[val] = post_data.get(key, '')

        data['num_cart_items'] = len(post_data.getlist('shopping-cart.items'))
        data['cart_items']     = self.gc_cart_items_blob(post_data)
    
        try:
            resp = GCNewOrderNotification.objects.create(**data)
            transaction_was_successful.send(sender=self.__class__, type="purchase", response=resp)
            status = "SUCCESS"
        except:
            transaction_was_unsuccessful.send(sender=self.__class__, type="purchase", response=post_data)
            status = "FAILURE"
        
        return HttpResponse(status)
    

    def custom_gc_new_order_notification(self, post_data,type):
        data = {}
        namespace="http://checkout.google.com/schema/2"
        resp_fields = {
            ".//{%s}google-order-number" % (namespace) : "google_order_number",
            ".//{%s}buyer-id"  % (namespace): "buyer_id",           
            ".//{%s}buyer-shipping-address/.//{%s}contact-name"  % (namespace,namespace): "shipping_contact_name",
            ".//{%s}buyer-billing-address/.//{%s}address1" % (namespace,namespace) : "shipping_address1",    
            ".//{%s}buyer-shipping-address/.//{%s}address2"  % (namespace,namespace): "shipping_address2",    
            ".//{%s}buyer-shipping-address/.//{%s}city"  % (namespace,namespace): "shipping_city",        
            ".//{%s}buyer-shipping-address/.//{%s}postal-code"  % (namespace,namespace): "shipping_postal_code", 
            ".//{%s}buyer-shipping-address/.//{%s}region"  % (namespace,namespace): "shipping_region",      
            ".//{%s}buyer-shipping-address/.//{%s}country-code"  % (namespace,namespace): "shipping_country_code",
            ".//{%s}buyer-shipping-address/.//{%s}email"  % (namespace,namespace): "shipping_email",       
            ".//{%s}buyer-shipping-address/.//{%s}company-name"  % (namespace,namespace): "shipping_company_name",
            ".//{%s}buyer-shipping-address/.//{%s}fax"  % (namespace,namespace): "shipping_fax",         
            ".//{%s}buyer-shipping-address/.//{%s}phone"  % (namespace,namespace): "shipping_phone",       
            ".//{%s}buyer-billing-address/.//{%s}contact-name"  % (namespace,namespace): "billing_contact_name",
            ".//{%s}buyer-billing-address/.//{%s}address1"  % (namespace,namespace): "billing_address1",    
            ".//{%s}buyer-billing-address/.//{%s}address2"  % (namespace,namespace): "billing_address2",    
            ".//{%s}buyer-billing-address/.//{%s}city"  % (namespace,namespace): "billing_city",        
            ".//{%s}buyer-billing-address/.//{%s}postal-code"  % (namespace,namespace): "billing_postal_code", 
            ".//{%s}buyer-billing-address/.//{%s}region"  % (namespace,namespace): "billing_region",      
            ".//{%s}buyer-billing-address/.//{%s}country-code"  % (namespace,namespace): "billing_country_code",
            ".//{%s}buyer-billing-address/.//{%s}email"  % (namespace,namespace): "billing_email",       
            ".//{%s}buyer-billing-address/.//{%s}company-name"  % (namespace,namespace): "billing_company_name",
            ".//{%s}buyer-billing-address/.//{%s}fax"  % (namespace,namespace): "billing_fax",         
            ".//{%s}buyer-billing-address/.//{%s}phone"  % (namespace,namespace): "billing_phone",       
            ".//{%s}buyer-marketing-preferences/.//{%s}email-allowed" % (namespace,namespace) : "marketing_email_allowed",
            ".//{%s}order-adjustment/.//{%s}total-tax"  % (namespace,namespace): "total_tax",                
            ".//{%s}order-adjustment/.//{%s}adjustment-total" % (namespace,namespace) : "adjustment_total",         
            ".//{%s}order-total" % (namespace) : "order_total",
            ".//{%s}financial-order-state"  % (namespace): "financial_order_state",  
            ".//{%s}fulfillment-order-state"  % (namespace): "fulfillment_order_state",
            ".//{%s}timestamp"  % (namespace): "timestamp",
        }
        resp_fields_atr = {
            ".//{%s}order-adjustment/.//{%s}total-tax" % (namespace,namespace) : "total_tax_currency",       
            ".//{%s}order-adjustment/.//{%s}adjustment-total"  % (namespace,namespace): "adjustment_total_currency",
            ".//{%s}order-total"  % (namespace): "order_total_currency",
        }
        
        data['notify_type'] =type
        data['serial_number'] =post_data.attrib['serial-number']
        for (key, val) in resp_fields.iteritems():
            data[val] = post_data.findtext(key)
        for (key, val) in resp_fields_atr.iteritems():
            data[val] = post_data.find(key).attrib['currency']
            
        data['num_cart_items'] = len(post_data.findall(".//{%s}shopping-cart/.//{%s}items"  % (namespace,namespace)))
        data['cart_items']     = self.custom_gc_cart_items_blob(post_data,namespace)
    
        try:
            resp = GCNewOrderNotification.objects.filter(serial_number=data['serial_number'])
            if resp:
                resp.update(**data)
                resp=resp[0]
                transactionnotification_was_successful.send(sender=self.__class__, type="purchase", response=resp)
            else:
                resp = GCNewOrderNotification.objects.create(**data)
                transaction_was_successful.send(sender=self.__class__, type="purchase", response=resp)
            status = "SUCCESS"
            #if resp.financial_order_state=='CHARGEABLE':charge_customer(resp)
        except:
            transaction_was_unsuccessful.send(sender=self.__class__, type="purchase", response=post_data)
            status = "FAILURE"
        
        return HttpResponse(status)

    def gc_order_state_change_notification(self, request):
        post_data = request.POST.copy()
        order = GCNewOrderNotification.objects.get(google_order_number=post_data['google-order-number'])
        order.financial_order_state = post_data['new-financial-order-state']
        order.fulfillment_order_state = post_data['new-fulfillment-order-state']
        order.save()
    
    def custom_gc_order_state_change_notification(self, post_data):
        namespace="http://checkout.google.com/schema/2"
        order = GCNewOrderNotification.objects.get(google_order_number=post_data.findtext( ".//{%s}google-order-number" % (namespace)))
        order.financial_order_state = post_data.findtext( ".//{%s}new-financial-order-state" % (namespace))
        order.fulfillment_order_state =post_data.findtext( ".//{%s}new-fulfillment-order-state" % (namespace))  
        order.save()
        transactionnotification_was_successful.send(sender=self.__class__, type="purchase", response=order)
        if order.financial_order_state=='CHARGEABLE':charge_customer(order)
        
    def custom_gc_order_charge_notification(self, post_data):
        namespace="http://checkout.google.com/schema/2"
        order = GCNewOrderNotification.objects.get(google_order_number=post_data.findtext( ".//{%s}google-order-number" % (namespace)))
        transactionnotification_was_successful.send(sender=self.__class__, type="purchase", response=order)

@csrf_exempt
@require_POST
def gc_notify_handler(request):
    p_config=PaymentConfigure.get_payment_settings()
    details={'merchant_id':str(p_config.merchant_id),'merchant_key':str(p_config.merchant_key)}
    google_checkout_obj=GoogleCheckoutIntegration(details)
    respond_xml=get_checkout_notification(request.POST['serial-number'],details)
    post_data = fromstring(respond_xml)
    type=post_data.tag.split('}')[1]
    
    if type=='new-order-notification':
        google_checkout_obj.custom_gc_new_order_notification(post_data,type)
    elif type == 'order-state-change-notification':
        google_checkout_obj.custom_gc_order_state_change_notification(post_data)
    elif type=="charge-amount-notification":
        google_checkout_obj.custom_gc_order_charge_notification(post_data)
    
    """
    if request.POST['_type'] == 'new-order-notification':
        google_checkout_obj.gc_new_order_notification(request)
    elif request.POST['_type'] == 'order-state-change-notification':
        google_checkout_obj.gc_order_state_change_notification(request)
    """  
    return HttpResponse(respond_xml)


def get_checkout_notification(serial_no,details):
    m_id=details['merchant_id']
    m_key=details['merchant_key']
    response = cStringIO.StringIO()
    c = pycurl.Curl() 
    c.setopt(c.URL,"https://sandbox.google.com/checkout/api/checkout/v2/reports/Merchant/"+str(m_id))
    c.setopt(c.HTTPHEADER, ["Content-type: application/xml; charset=UTF-8","Accept: application/xml; charset=UTF-8"])
    c.setopt(c.USERPWD, str(m_id)+":"+str(m_key))
    c.setopt(c.TIMEOUT, 4)
    c.setopt(c.POST, 1)
    request='<?xml version="1.0" encoding="UTF-8"?><notification-history-request xmlns="http://checkout.google.com/schema/2"><serial-number>'+str(serial_no)+'</serial-number></notification-history-request>'
    c.setopt(c.POSTFIELDS, request);
    c.setopt(c.WRITEFUNCTION, response.write)
    c.perform()
    c.close()
    return response.getvalue()

def charge_customer(order):
    p_config=PaymentConfigure.get_payment_settings()
    m_id=str(p_config.merchant_id)
    m_key=str(p_config.merchant_key)
    response = cStringIO.StringIO()
    c = pycurl.Curl() 
    c.setopt(c.URL,"https://sandbox.google.com/checkout/api/checkout/v2/requestForm/Merchant/"+str(m_id))
    c.setopt(c.HTTPHEADER, ["Content-type: application/xml; charset=UTF-8","Accept: application/xml; charset=UTF-8"])
    c.setopt(c.USERPWD, str(m_id)+":"+str(m_key))
    c.setopt(c.TIMEOUT, 4)
    c.setopt(c.POST, 1)
    request="_type=charge-and-ship-order&google-order-number="+str(order.google_order_number)+"&amount="+str(order.order_total)+"&amount.currency="+str(order.order_total_currency)+"&send-email=true"
    c.setopt(c.POSTFIELDS, request);
    c.setopt(c.WRITEFUNCTION, response.write)
    c.perform()
    c.close()
    return response.getvalue()



