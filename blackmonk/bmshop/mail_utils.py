import HTMLParser

from django.conf import settings as my_settings
from django.core.mail import EmailMessage
from django.template import  Template,Context
from django.template.loader import render_to_string

from usermgmt.models import EmailTemplates
from common.utils import get_global_settings
from bmshop.shop.models import Shop


def send_mail_order(order):
    global_settings=get_global_settings()
    try:
        item_all = ''
        items = order.get_order_items()
        for item in items:
            item_name = '* %s (%s qty).<br/> '%(item.product_name,str(int(item.quantity)))
            item_all+=item_name 
        
        address = '%s<br/>'%(order.name)
        address+= '%s<br/> '%(order.address.strip())
        address+= '%s-%s<br/> '%(order.city,order.zip_code)
        address+= '%s<br/> '%(order.state)
        if order.phone:
            address+= order.phone
        
        to_emailids = [order.email]
        email_temp = EmailTemplates.objects.get(code='soc')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({
                "USERNAME": order.name,
                "ORDER_ID": order.order_number,
                "PRICE": global_settings.currency+str(order.price),
                "ITEMS": item_all,
                "DELIVERY_ADDRESS": address,
                "WEBSITE": global_settings.domain,
                "ORDER_URL":'%s/user/shop/orders'%(global_settings.website_url)
                    })
        email_message=t.render(c)
        
        parse = HTMLParser.HTMLParser()
        email_message = parse.unescape(email_message)
        
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass
    
    
def send_mail_shippment(order):
    global_settings=get_global_settings()
    try:
        item_all = ''
        items = order.get_order_items()
        for item in items:
            item_name = '* %s (%s qty).<br/> '%(item.product_name,str(int(item.quantity)))
            item_all+=item_name 
        
        address = '%s<br/>'%(order.name)
        address+= '%s<br/> '%(order.address.strip())
        address+= '%s-%s<br/> '%(order.city,order.zip_code)
        address+= '%s<br/> '%(order.state)
        if order.phone:
            address+= order.phone
        
        to_emailids = [order.email]
        email_temp = EmailTemplates.objects.get(code='ssc')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({
                "USERNAME": order.name,
                "ORDER_ID": order.order_number,
                "PRICE": global_settings.currency+str(order.price),
                "ITEMS": item_all,
                "SHIPPING_METHOD": order.shipping_method,
                "DELIVERY_ADDRESS": address,
                "WEBSITE": global_settings.domain,
                "ORDER_URL":'%s/user/shop/orders'%(global_settings.website_url)
                    })
        email_message=t.render(c)
        
        parse = HTMLParser.HTMLParser()
        email_message = parse.unescape(email_message)
        
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass    
    
def send_mail_delivery(order):
    global_settings=get_global_settings()
    try:
        item_all = ''
        items = order.get_order_items()
        for item in items:
            item_name = '* %s (%s qty).<br/> '%(item.product_name,str(int(item.quantity)))
            item_all+=item_name 
        
        to_emailids = [order.email]
        email_temp = EmailTemplates.objects.get(code='sdc')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({
                "USERNAME": order.name,
                "ORDER_ID": order.order_number,
                "ITEMS": item_all,
                "WEBSITE": global_settings.domain,
                    })
        email_message=t.render(c)
        
        parse = HTMLParser.HTMLParser()
        email_message = parse.unescape(email_message)
        
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass 
    
def send_notify(order):
    global_settings=get_global_settings()
    shop_obj = Shop.get_shop_settings()
    try:
        to_emailids = shop_obj.notification_emails.split(',')
        mail_subject="Item Purchased [Order Id: %s]"%(order.order_number)
        mail_message = render_to_string("bmshop/staff/notify_email.html",{'order':order,'global_settings':global_settings})
        msg = EmailMessage(mail_subject, mail_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        msg.content_subtype = "html"  
        msg.send()
    except:
        pass
            