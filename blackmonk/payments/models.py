from datetime import date
import datetime, json
from dateutil.relativedelta import relativedelta

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.views.decorators.csrf import csrf_exempt

from payments.paypal.standard.ipn.signals import payment_was_successful,payment_was_updated
from payments.paypal.standard.ipn.models import PayPalIPN
from payments.paypal.standard.pdt.signals import pdt_successful
from payments.googlecheckout.views import transaction_was_successful,transactionnotification_was_successful
from payments.authorizenet import signals as auth_net

from article.models import Article
from business.models import Business,BusinessPrice,BusinessClaim,BusinessClaimSettings
from business.utils import save_to_claim_business
from classifieds.models import Classifieds,ClassifiedPrice
from events.models import Event,EventPrice

from deal.models import Deal,DealPayment
from deal.utils import buy_success_mail,send_voucher_mail,buy_success_gift_mail
from deal.utils import send_voucher_mail
from bmshop.order.models import Order
from bmshop.cart.models import Cart
from bmshop.mail_utils import send_mail_order,send_notify

from common.models import ApprovalSettings
from common.mail_utils import mail_publish_classifieds,mail_publish_business,mail_publish_event,mail_publish_article,mail_publish_banner

from common import signals
from banners.models import BannerZones, BannerAdvertisements, BannerSections, BannerReports, BannerPayment
from django.contrib.auth import get_user_model

User = get_user_model()
PAYMENT_MODE = (('Paypal','Paypal'),
                 ('Offline','Offline'),)

ORDER_STATUS = (('Success','Success'),
                  ('Failed','Failed'),
                  ('Cancelled','Cancelled'),)
 
class PaymentOrder(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    invoice_no = models.CharField(max_length=75)
    transactionid = models.CharField(max_length=50,null=True)
    txn_type = models.CharField("Transaction Type", max_length=128, blank=True, help_text="PayPal transaction type.")
    payment_mode = models.CharField(choices=PAYMENT_MODE,max_length=25)
    status = models.CharField(choices=ORDER_STATUS,max_length=25)
    amount = models.FloatField(default=0.0)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    user = models.ForeignKey(User)
    listing_type = models.CharField(max_length=50, blank=True,null=True)
    object_name = models.CharField(max_length=300,blank=True,null=True)
    offline_mode = models.CharField(max_length=500,blank=True,null=True)
    contact_mode = models.CharField(max_length=50, null=True)
    phone_no = models.CharField(max_length=25, null=True)
    email = models.EmailField(null=True)
    cheque_dd_num = models.CharField(max_length=50, null=True)
    
    def get_pay_obj(self):
        try:return PayPalIPN.objects.get(txn_id=self.transactionid).subscr_id
        except:return None

class OfflinePayment(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    amount = models.FloatField(default=0.0)
    moredetails = models.TextField()

    status = models.CharField(max_length=1, default='N')  # N-pending, P-Approved, B-BlockedByStaff, D-CancelledByUser, E-Expired/Timeout
    processed_by = models.ForeignKey(User, related_name='staff', null=True, blank=True)
    posted_date = models.DateTimeField('posted_date', auto_now_add=True)
    expiry_date = models.DateTimeField('expiry_date')
    approved_date = models.DateTimeField('approved_date', null=True, blank=True)
    
    def get_moredetails(self):
        if self.moredetails:
            return json.loads(self.moredetails)
    
    def get_value(self, key):
        if self.moredetails:
            data = json.loads(self.moredetails)
            return data.get(key)
    
    def get_status(self):
        return {'N': 'Pending', 'P': 'Approved', 'B': 'BlockedByStaff', 'D': 'CancelledByUser', 'E': 'Expired/Timeout'}[self.status]

@csrf_exempt
def update_order(sender, **kwargs):
    start_date=end_date=None
    object_name=''
    pdt_obj = sender
    custom = pdt_obj.custom.split(":")
    try:
        user=User.objects.get(pk=custom[3])
    except:user=None
    
    if custom[0] == 'event':
        approval_settings=ApprovalSettings.objects.get(name='events')
        ct = ContentType.objects.get_for_model(Event)
        id = custom[1]
        event=Event.objects.get(pk=id)
        if event.status=='D':
            signals.create_staffmail.send(sender=None,object=event,module='events',action='A',user=user)
        else:
            signals.create_staffmail.send(sender=None,object=event,module='events',action='UG',user=user)
        if approval_settings.paid and pdt_obj.is_completed:
            event.status='P'
            try:mail_publish_event(event)
            except:pass
        else:event.status='N'
        
        try:
            event_price_obj = EventPrice.objects.get(level=str(custom[2]))
            event.payment=event_price_obj
        except:pass
        if str(custom[2])=='level2':
            event.listing_type='F'
            custom[2]='Featured Event '
        elif str(custom[2])=='level1':
            event.listing_type='S'
            custom[2]='Sponsored Event'
        event.listing_duration=custom[4]
        
        try:
            sdate=custom[5].split('/')
            edate=custom[6].split('/')
            event.listing_start=datetime.datetime(int(sdate[0]),int(sdate[1]),int(sdate[2]))
            event.listing_end=datetime.datetime(int(edate[0]),int(edate[1]),int(edate[2]))
        except:
            sdate=custom[5].split('-')
            edate=custom[6].split('-')
            event.listing_start=datetime.datetime(int(sdate[0]),int(sdate[1]),int(sdate[2]))
            event.listing_end=datetime.datetime(int(edate[0]),int(edate[1]),int(edate[2]))
        try:
            if pdt_obj.payment_gross:event.listing_price=pdt_obj.payment_gross
            else:event.listing_price = pdt_obj.mc_gross
        except:event.listing_price = pdt_obj.mc_gross
        event.save()
        notifictn_type = 'listed as '+event_price_obj.level_label.lower()+' in'
        signals.create_notification.send(sender=None,user=event.created_by, obj=event, not_type=notifictn_type,obj_title=event.title)    
        start_date=event.listing_start
        end_date=event.listing_end
        object_name=event.get_payment_title()
        
    elif custom[0] == 'business':
        appreoval_settings = ApprovalSettings.objects.get(name='business')
        ct = ContentType.objects.get_for_model(Business)
        id = custom[1]
        business_obj=Business.objects.get(pk=id)
        if str(custom[4])=='1' and pdt_obj.is_completed:
            #############################CLAIM######################################
            claimsettings=BusinessClaimSettings.get_setting()
            if ( claimsettings.auto_aprove_paid_buz_claim and business_obj.featured_sponsored in ['F', 'S'] ) or \
                ( claimsettings.auto_aprove_free_buz_claim and business_obj.featured_sponsored == 'B' ):
                save_to_claim_business(business=business_obj, approve=True, paid=True)
            else:
                save_to_claim_business(business=business_obj, approve=False, paid=True)
            if business_obj.status == 'P':
                try:mail_publish_business(business_obj)
                except:pass
            signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='C',user=user)
        else:
            if business_obj.status=='D':
                signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='A',user=user)
            else:
                signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='UG',user=user)
        if appreoval_settings.paid and pdt_obj.is_completed:
            business_obj.status='P'
            try:mail_publish_business(business_obj)
            except:pass
        else:
            business_obj.status='N'
        try:
            if pdt_obj.payment_gross:business_obj.sp_cost=pdt_obj.payment_gross
            else:business_obj.sp_cost = pdt_obj.mc_gross
        except:business_obj.sp_cost = pdt_obj.mc_gross
       
        business_price_obj = BusinessPrice.objects.get(level = str(custom[2]))
        business_obj.payment=business_price_obj
        business_obj.lstart_date=date.today()
        if business_obj.payment_type == 'Y':business_obj.lend_date=date.today()+relativedelta(years=+1)
        else:business_obj.lend_date=date.today()+relativedelta(months=+1)
        
        if str(custom[2])=='level2':
            business_obj.featured_sponsored='F'
            custom[2]='Featured Business'
        elif str(custom[2])=='level1':
            business_obj.featured_sponsored='S'
            custom[2]='Sponsored Business'
        business_obj.is_paid=True
        business_obj.save()
        notifictn_type = 'listed as '+business_price_obj.level_label.lower()+' in'
        signals.create_notification.send(sender=None,user=business_obj.created_by, obj=business_obj, not_type=notifictn_type,obj_title=business_obj.name)  
        
        start_date=business_obj.lstart_date
        end_date=business_obj.lend_date
        object_name=business_obj.get_payment_title()
        
    elif custom[0] == 'classifieds':
        approval_settings=ApprovalSettings.objects.get(name='classifieds')
        ct = ContentType.objects.get_for_model(Classifieds)
        id = custom[1]
        classifieds_obj=Classifieds.objects.get(pk=id)
        
        if classifieds_obj.status=='D':
            signals.create_staffmail.send(sender=None,object=classifieds_obj,module='classifieds',action='A',user=user)
        else:
            signals.create_staffmail.send(sender=None,object=classifieds_obj,module='classifieds',action='UG',user=user)
        
        if approval_settings.paid and pdt_obj.is_completed:
            classifieds_obj.status='P'
            try:mail_publish_classifieds(classifieds_obj)
            except:pass
        else:classifieds_obj.status='N'

        classifieds_price_obj = ClassifiedPrice.objects.get(level =str(custom[2]))
        period=classifieds_price_obj.contract_period
        
        classifieds_obj.payment=classifieds_price_obj
        classifieds_obj.listing_start_date=date.today()
        classifieds_obj.listing_end_date=date.today()+relativedelta(months=+period)
        classifieds_obj.published_on=datetime.datetime.now()
        
        try:
            if pdt_obj.payment_gross:classifieds_obj.price=pdt_obj.payment_gross
            else:classifieds_obj.price = pdt_obj.mc_gross
        except:classifieds_obj.price = pdt_obj.mc_gross
        #classifieds_obj.payment_type=pdt_obj.payment_cycle
        if classifieds_price_obj.level=='level2':
            classifieds_obj.listing_type='F'
            custom[2]='Featured Classified'
        elif classifieds_price_obj.level=='level1':
            classifieds_obj.listing_type='S'
            custom[2]='Sponsored Classified'
        classifieds_obj.is_paid=True
        classifieds_obj.save()  
        notifictn_type = 'posted as '+classifieds_price_obj.level_label.lower()+' in'
        signals.create_notification.send(sender=None,user=classifieds_obj.created_by, obj=classifieds_obj, not_type=notifictn_type,obj_title=classifieds_obj.title) 
        start_date=classifieds_obj.listing_start_date
        end_date=classifieds_obj.listing_end_date
        object_name=classifieds_obj.get_payment_title()
    
    elif custom[0] == 'deal':
        ct = ContentType.objects.get_for_model(Deal)
        #addr=GiftedAddress.objects.get()
        id = custom[1]
        deal = Deal.objects.get(pk = id)
        deal_payment = DealPayment.objects.get(pk = custom[2])
        deal_payment.status = 'S'
            
        deal_payment.transaction_no = pdt_obj.txn_id
        deal_payment.is_paid = True
        deal_payment.payment_status = pdt_obj.payment_status
        deal_payment.payer_status = pdt_obj.payer_status
        deal_payment.transaction_type = pdt_obj.txn_type
        deal_payment.save()
        user=deal_payment.created_by
        signals.create_notification.send(sender=None,user=deal_payment.created_by, obj=deal, not_type='bought as',obj_title=deal.title) 
        signals.create_staffmail.send(sender=None,object=deal,module='deals',action='P',user=user)
        custom[2]='Purchased Deal(s)'
        if deal_payment.is_friend: 
            buy_success_gift_mail(deal_payment,deal)
            send_voucher_mail(deal_payment,deal,deal_payment.gift_addr.g_email)
        else:
            buy_success_mail(deal_payment,deal)
            send_voucher_mail(deal_payment,deal,deal_payment.email)
        object_name=deal.get_payment_title()
    
    elif custom[0] == 'banners':
        ct = ContentType.objects.get_for_model(BannerAdvertisements)
        #addr=GiftedAddress.objects.get()
        id = custom[1]
        banner_obj = BannerAdvertisements.objects.get(pk = id)
        banner_obj_payment = BannerPayment.objects.get(level = custom[2])
        custom[2]=str(banner_obj_payment.level)+" banner"
        user=banner_obj.created_by
        signals.create_notification.send(sender=None,user=banner_obj_payment.created_by, obj=banner_obj, not_type='bought as',obj_title=banner_obj.caption) 
        signals.create_staffmail.send(sender=None,object=banner_obj,module='banners',action='P',user=user)
        object_name=banner_obj.get_payment_title()
    
    elif custom[0] == 'article':
        approval_settings=ApprovalSettings.objects.get(name='article')
        ct = ContentType.objects.get_for_model(Article)
        id = custom[1]
        article_obj=Article.objects.get(pk = id)
        if approval_settings.paid and pdt_obj.is_completed:
            article_obj.status='P'
            try:mail_publish_article(article_obj)
            except:pass
        else:article_obj.status='N'
        article_obj.save()
        signals.create_notification.send(sender=None,user=article_obj.created_by, obj=article_obj, not_type='submitted in',obj_title=article_obj.title)
        signals.create_staffmail.send(sender=None,object=article_obj,module='articles',action='A',user=user)
        if custom[2]=='FR':custom[2]='Article Own Story'
        elif custom[2]=='PR':custom[2]='Article Pressrelease'
        elif custom[2]=='A':custom[2]='Article Advertorial'
        elif custom[2]=='RR':custom[2]='Article Review Request'
        object_name=article_obj.get_payment_title()
    
    elif custom[0] == 'shop':
        ct = ContentType.objects.get_for_model(Order)
        id = custom[1]
        order_obj=Order.objects.get(pk = id)
        order_obj.transaction_id = pdt_obj.txn_id
        if pdt_obj.payment_status == 'Pending':
            order_obj.status = 4
        elif pdt_obj.payment_status == 'Cancelled':
            order_obj.status = 2     
        elif pdt_obj.is_completed:
            order_obj.status = 1 
            try:
                cart = Cart.objects.get(user_id=order_obj.user.id)
                cart.delete()
            except:pass 
            send_mail_order(order_obj)  
        else:
            order_obj.status = 3   
        order_obj.payment_method = 'PP'  
        order_obj.payment_price = pdt_obj.payment_gross
        order_obj.save()
        send_notify(order_obj)
    try:po = PaymentOrder.objects.get(transactionid=pdt_obj.txn_id)
    except:po = PaymentOrder()
    po.content_type=ct
    po.object_id= id
    po.invoice_no=pdt_obj.invoice
    po.transactionid=pdt_obj.txn_id
    po.txn_type=pdt_obj.txn_type
    po.payment_mode='Paypal'
    try:
        if pdt_obj.payment_gross:po.amount=pdt_obj.payment_gross
        else:po.amount=pdt_obj.mc_gross
    except:po.amount=pdt_obj.mc_gross
    try:po.listing_type=custom[2]
    except:pass
    po.user=user
    if pdt_obj.payment_status=='Completed':po.status='Success'
    else:po.status='Pending'
    try:
        if start_date:po.start_date=start_date
        if end_date:po.end_date=end_date 
    except:pass
    po.object_name=object_name
    po.save()

@csrf_exempt    
def update_order_notification(sender, **kwargs):
    start_date=end_date=None
    object_name=''
    pdt_obj = sender
    custom = pdt_obj.custom.split(":")
    try:user=User.objects.get(pk=custom[3])
    except:user=None
    if custom[0] == 'event':
        approval_settings=ApprovalSettings.objects.get(name='events')
        ct = ContentType.objects.get_for_model(Event)
        id = custom[1]
        event=Event.objects.get(pk=id)
        if event.status=='D':
            signals.create_staffmail.send(sender=None,object=event,module='events',action='A',user=user)
        else:
            signals.create_staffmail.send(sender=None,object=event,module='events',action='UG',user=user)
        if approval_settings.paid and pdt_obj.payment_status=='Completed':
            event.status='P'
            try:mail_publish_event(event)
            except:pass
        else:
            event.status='N'
        
        try:
            event_price_obj = EventPrice.objects.get(level=str(custom[2]))
            event.payment=event_price_obj
        except:pass
        if str(custom[2])=='level2':
            event.listing_type='F'
            custom[2]='Featured Event '
        elif str(custom[2])=='level1':
            event.listing_type='S'
            custom[2]='Sponsored Event'
        event.listing_duration=custom[4]
        try:
            sdate=custom[5].split('/')
            edate=custom[6].split('/')
            event.listing_start=datetime.datetime(int(sdate[0]),int(sdate[1]),int(sdate[2]))
            event.listing_end=datetime.datetime(int(edate[0]),int(edate[1]),int(edate[2]))
        except:
            sdate=custom[5].split('-')
            edate=custom[6].split('-')
            event.listing_start=datetime.datetime(int(sdate[0]),int(sdate[1]),int(sdate[2]))
            event.listing_end=datetime.datetime(int(edate[0]),int(edate[1]),int(edate[2]))
        try:
            if pdt_obj.payment_gross:event.listing_price=pdt_obj.payment_gross
            else:event.listing_price = pdt_obj.mc_gross
        except:event.listing_price = pdt_obj.mc_gross
        event.save()
        notifictn_type = 'listed as '+event_price_obj.level_label.lower()+' in'
        signals.create_notification.send(sender=None,user=event.created_by, obj=event, not_type=notifictn_type,obj_title=event.title)    
        start_date=event.listing_start
        end_date=event.listing_end
        object_name=event.get_payment_title()
        
    elif custom[0] == 'business':
        appreoval_settings = ApprovalSettings.objects.get(name='business')
        ct = ContentType.objects.get_for_model(Business)
        id = custom[1]
        business_obj=Business.objects.get(pk=id)
        try:
            #############################CLAIM######################################
            if str(custom[4])=='1':
                save_to_claim_business(user,business_obj,True,True)
                signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='C',user=user)
            #############################CLAIM######################################
                claim=BusinessClaim.objects.get(business=business_obj)
                claimsettings=BusinessClaimSettings.get_setting()
                if claimsettings.auto_aprove_paid_buz_claim:
                    claim.is_approved=True
                    claim.save()
                    business_obj.created_by=claim.user
                    business_obj.status='P'
                    try:mail_publish_business(business_obj)
                    except:pass
                else:business_obj.status='N'
            else:
                if business_obj.status=='D':
                    signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='A',user=user)
                else:
                    signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='UG',user=user)
                if appreoval_settings.paid:
                    business_obj.status='P'
                    try:mail_publish_business(business_obj)
                    except:pass
                else:
                    business_obj.status='N'
        except:
            if business_obj.status=='D':
                signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='A',user=user)
            else:
                signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='UG',user=user)
            if appreoval_settings.paid:
                business_obj.status='P'
                try:mail_publish_business(business_obj)
                except:pass
            else:
                business_obj.status='N'
       
        if pdt_obj.txn_type in ["subscr_cancel","subscr_eot","subscr_failed"]:
            buz_settings=BusinessClaimSettings.get_settings()
            if buz_settings.after_failed_payment=='B':business_obj.status='B'
            else:business_obj.featured_sponsored='B'
        else:business_obj.status='P'
        
        try:
            if pdt_obj.payment_gross:business_obj.sp_cost=pdt_obj.payment_gross
            else:business_obj.sp_cost = pdt_obj.mc_gross
        except:business_obj.sp_cost = pdt_obj.mc_gross
       
        business_price_obj = BusinessPrice.objects.get(level = str(custom[2]))
        business_obj.payment=business_price_obj
        business_obj.lstart_date=date.today()
        if business_obj.payment_type == 'Y':business_obj.lend_date=date.today()+relativedelta(years=+1)
        else:business_obj.lend_date=date.today()+relativedelta(months=+1)
        
        if str(custom[2])=='level2':
            business_obj.featured_sponsored='F'
            custom[2]='Featured Business'
        elif str(custom[2])=='level1':
            business_obj.featured_sponsored='S'
            custom[2]='Sponsored Business'
        business_obj.is_paid=True
        business_obj.save()
        notifictn_type = 'listed as '+business_price_obj.level_label.lower()+' in'
        signals.create_notification.send(sender=None,user=business_obj.created_by, obj=business_obj, not_type=notifictn_type,obj_title=business_obj.name)  
        
        start_date=business_obj.lstart_date
        end_date=business_obj.lend_date
        object_name=business_obj.get_payment_title()
        
    elif custom[0] == 'classifieds':
        approval_settings=ApprovalSettings.objects.get(name='classifieds')
        ct = ContentType.objects.get_for_model(Classifieds)
        id = custom[1]
        classifieds_obj=Classifieds.objects.get(pk=id)
        
        if classifieds_obj.status=='D':
            signals.create_staffmail.send(sender=None,object=classifieds_obj,module='classifieds',action='A',user=user)
        else:
            signals.create_staffmail.send(sender=None,object=classifieds_obj,module='classifieds',action='UG',user=user)
        
        if approval_settings.paid and pdt_obj.payment_status=='Completed':
            classifieds_obj.status='P'
            try:mail_publish_classifieds(classifieds_obj)
            except:pass
        else:
            classifieds_obj.status='N'

        classifieds_price_obj = ClassifiedPrice.objects.get(level =str(custom[2]))
        period=classifieds_price_obj.contract_period
        
        classifieds_obj.payment=classifieds_price_obj
        classifieds_obj.listing_start_date=date.today()
        classifieds_obj.listing_end_date=date.today()+relativedelta(months=+period)
        
        try:
            if pdt_obj.payment_gross:classifieds_obj.price=pdt_obj.payment_gross
            else:classifieds_obj.price = pdt_obj.mc_gross
        except:classifieds_obj.price = pdt_obj.mc_gross
        #classifieds_obj.payment_type=pdt_obj.payment_cycle
        if classifieds_price_obj.level=='level2':
            classifieds_obj.listing_type='F'
            custom[2]='Featured Classified'
        elif classifieds_price_obj.level=='level1':
            classifieds_obj.listing_type='S'
            custom[2]='Sponsored Classified'
        classifieds_obj.is_paid=True
        classifieds_obj.save()  
        notifictn_type = 'posted as '+classifieds_price_obj.level_label.lower()+' in'
        signals.create_notification.send(sender=None,user=classifieds_obj.created_by, obj=classifieds_obj, not_type=notifictn_type,obj_title=classifieds_obj.title) 
        start_date=classifieds_obj.listing_start_date
        end_date=classifieds_obj.listing_end_date
        object_name=classifieds_obj.get_payment_title()
    
    elif custom[0] == 'deal':
        ct = ContentType.objects.get_for_model(Deal)
        #addr=GiftedAddress.objects.get()
        id = custom[1]
        deal = Deal.objects.get(pk = id)
        deal_payment = DealPayment.objects.get(pk = custom[2])
        deal_payment.status = 'S'
            
        deal_payment.transaction_no = pdt_obj.txn_id
        deal_payment.is_paid = True
        deal_payment.payment_status = pdt_obj.payment_status
        deal_payment.payer_status = pdt_obj.payer_status
        deal_payment.transaction_type = pdt_obj.txn_type
        deal_payment.save()
        user=deal_payment.created_by
        signals.create_notification.send(sender=None,user=deal_payment.created_by, obj=deal, not_type='bought as',obj_title=deal.title) 
        signals.create_staffmail.send(sender=None,object=deal,module='deals',action='P',user=user)
        custom[2]='Purchased Deal(s)'
        if deal_payment.is_friend: 
            buy_success_gift_mail(deal_payment,deal)
            send_voucher_mail(deal_payment,deal,deal_payment.gift_addr.g_email)
        else:
            buy_success_mail(deal_payment,deal)
            send_voucher_mail(deal_payment,deal,deal_payment.email)
        object_name=deal.get_payment_title()
    
    elif custom[0] == 'banners':
        approval_settings=ApprovalSettings.objects.get(name='banners')
        ct = ContentType.objects.get_for_model(BannerAdvertisements)
        id = custom[1]
        banner_obj=BannerAdvertisements.objects.get(pk = id)
        if approval_settings.paid and pdt_obj.payment_status=='Completed':
            banner_obj.status='P'
            try:mail_publish_banner(banner_obj)
            except:pass
        else:
            banner_obj.status='N'
        banner_obj.save()
        signals.create_notification.send(sender=None,user=banner_obj.created_by, obj=banner_obj, not_type='submitted in',obj_title=banner_obj.title)
        signals.create_staffmail.send(sender=None,object=banner_obj,module='banners',action='A',user=user)
        object_name=banner_obj.get_payment_title()
    
    elif custom[0] == 'article':
        approval_settings=ApprovalSettings.objects.get(name='article')
        ct = ContentType.objects.get_for_model(Article)
        id = custom[1]
        article_obj=Article.objects.get(pk = id)
        if approval_settings.paid and pdt_obj.payment_status=='Completed':
            article_obj.status='P'
            try:mail_publish_article(article_obj)
            except:pass
        else:
            article_obj.status='N'
        article_obj.save()
        signals.create_notification.send(sender=None,user=article_obj.created_by, obj=article_obj, not_type='submitted in',obj_title=article_obj.title)
        signals.create_staffmail.send(sender=None,object=article_obj,module='articles',action='A',user=user)
        if custom[2]=='FR':custom[2]='Article Own Story'
        elif custom[2]=='PR':custom[2]='Article Pressrelease'
        elif custom[2]=='A':custom[2]='Article Advertorial'
        elif custom[2]=='RR':custom[2]='Article Review Request'
        object_name=article_obj.get_payment_title()
    
    elif custom[0] == 'shop':
        ct = ContentType.objects.get_for_model(Order)
        id = custom[1]
        order_obj=Order.objects.get(pk = id)
        order_obj.transaction_id = pdt_obj.txn_id
        if pdt_obj.payment_status == 'Pending':
            order_obj.status = 4
        elif pdt_obj.payment_status == 'Cancelled':
            order_obj.status = 2     
        elif pdt_obj.payment_status == 'Completed':
            order_obj.status = 1
            try:
                cart = Cart.objects.get(user_id=order_obj.user.id)
                cart.delete()
            except:pass    
            send_mail_order(order_obj)  
        else:
            order_obj.status = 3   
        order_obj.payment_method = 'PP'  
        order_obj.payment_price = pdt_obj.payment_gross
        order_obj.save()
        object_name = "Order Items"
        send_notify(order_obj) 
        
    try:po = PaymentOrder.objects.get(transactionid=pdt_obj.txn_id)
    except:po = PaymentOrder()
    po.content_type=ct
    po.object_id= id
    po.invoice_no=pdt_obj.invoice
    po.transactionid=pdt_obj.txn_id
    po.txn_type=pdt_obj.txn_type
    po.payment_mode='Paypal'
    try:
        if pdt_obj.payment_gross:po.amount=pdt_obj.payment_gross
        else:po.amount = pdt_obj.mc_gross
    except:po.amount = pdt_obj.mc_gross
    try:po.listing_type=custom[2]
    except:pass
    po.user=user
    if pdt_obj.payment_status=='Completed':po.status='Success'
    else:po.status='Pending'
    if start_date:po.start_date=start_date
    if end_date:po.end_date=end_date 
    po.object_name=object_name
    po.save()
    
    
"""
##################################################################################################################################
##################################################################################################################################
############################################        Google Checkout     ##########################################################
##################################################################################################################################
##################################################################################################################################
"""


def update_order_gc(sender,**kwargs):
    start_date=end_date=None
    object_name=''
    obj=kwargs['response']
    gc_obj=obj.cart_items
    gc_obj=gc_obj.split('#@#')[0]
    gc_obj=gc_obj.split(':#')
    model=gc_obj[0]
    object_id=gc_obj[1]
    invoice=gc_obj[2]
    payment_level=gc_obj[3]
    user=User.objects.get(pk=gc_obj[4])
    
    status=obj.financial_order_state
    if status=='CHARGED':state='Success'
    else:state='Pending'
    
    
    if model == 'classifieds':
        approval_settings=ApprovalSettings.objects.get(name='classifieds')
        ct = ContentType.objects.get_for_model(Classifieds)
        classifieds_obj=Classifieds.objects.get(pk=object_id)
        
        if state=='Success' and classifieds_obj.status=='D':
            signals.create_staffmail.send(sender=None,object=classifieds_obj,module='classifieds',action='A',user=user)
        elif state=='Success': 
            signals.create_staffmail.send(sender=None,object=classifieds_obj,module='classifieds',action='UG',user=user)
        
        if approval_settings.paid and state=='Success':
            classifieds_obj.status='P'
            try:mail_publish_classifieds(classifieds_obj)
            except:pass
        else:classifieds_obj.status='N'

        classifieds_price_obj = ClassifiedPrice.objects.get(level=payment_level)
        period=classifieds_price_obj.contract_period

        classifieds_obj.payment=classifieds_price_obj
        if state=='Success':  
            classifieds_obj.listing_start_date=date.today()
            classifieds_obj.listing_end_date=date.today()+relativedelta(months=+period)

        classifieds_obj.price=obj.order_total
        if classifieds_price_obj.level=='level2':
            classifieds_obj.listing_type='F'
            payment_level='Featured Classified'
        elif classifieds_price_obj.level=='level1':
            classifieds_obj.listing_type='S'
            payment_level='Sponsored Classified'
        classifieds_obj.is_paid=True
        classifieds_obj.save() 
        notifictn_type = 'posted as '+classifieds_price_obj.level_label.lower()+' in'
        signals.create_notification.send(sender=None,user=classifieds_obj.created_by, obj=classifieds_obj, not_type=notifictn_type,obj_title=classifieds_obj.title)  
        start_date=classifieds_obj.listing_start_date
        end_date=classifieds_obj.listing_end_date
        object_name=classifieds_obj.get_payment_title()
    
    elif model == 'business':
        appreoval_settings = ApprovalSettings.objects.get(name='business')
        ct = ContentType.objects.get_for_model(Business)
        business_obj=Business.objects.get(pk=object_id)
        try:
            #############################CLAIM######################################
            if business_obj.is_claimable:
                save_to_claim_business(user,business_obj,True,True)
                signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='C',user=user)
            #############################CLAIM######################################
                claim=BusinessClaim.objects.get(business=business_obj)
                claimsettings=BusinessClaimSettings.get_setting()
                
                
                if claimsettings.auto_aprove_paid_buz_claim:
                    claim.is_approved=True
                    claim.save()
                    business_obj.created_by=claim.user
                    business_obj.status='P'
                    try:mail_publish_business(business_obj)
                    except:pass
                else:business_obj.status='N'
            else:
                if business_obj.status=='D':
                    signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='A',user=user)
                else:
                    signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='UG',user=user)
                if appreoval_settings.paid:
                    business_obj.status='P'
                    try:mail_publish_business(business_obj)
                    except:pass
                else:business_obj.status='N'
        except:
            if business_obj.status=='D':
                signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='A',user=user)
            else:
                signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='UG',user=user)
            if appreoval_settings.paid:
                business_obj.status='P'
                try:mail_publish_business(business_obj)
                except:pass
            else:business_obj.status='N'
       
        if state=='Success' and business_obj.is_claimable:
            buz_settings=BusinessClaimSettings.get_settings()
            if buz_settings.after_failed_payment=='B':business_obj.status='B'
            else:business_obj.featured_sponsored='B'
        else:business_obj.status='P'
        
        business_obj.sp_cost=obj.order_total
       
        business_price_obj = BusinessPrice.objects.get(level = payment_level)
        business_obj.payment=business_price_obj
        business_obj.lstart_date=date.today()
        if business_obj.payment_type == 'Y':business_obj.lend_date=date.today()+relativedelta(years=+1)
        else:business_obj.lend_date=date.today()+relativedelta(months=+1)
        
        if business_price_obj.level=='level2':
            business_obj.featured_sponsored='F'
            payment_level='Featured Business'
        elif business_price_obj.level=='level1':
            business_obj.featured_sponsored='S'
            payment_level='Sponsored Business'
        business_obj.is_paid=True
        business_obj.save()
        notifictn_type = 'listed as '+business_price_obj.level_label.lower()+' in'
        signals.create_notification.send(sender=None,user=business_obj.created_by, obj=business_obj, not_type=notifictn_type,obj_title=business_obj.name)  
        
        start_date=business_obj.lstart_date
        end_date=business_obj.lend_date
        object_name=business_obj.get_payment_title()
   
    elif model == 'article':
        approval_settings=ApprovalSettings.objects.get(name='article')
        ct = ContentType.objects.get_for_model(Article)
        article_obj=Article.objects.get(pk = object_id)
        
        if state=='Success' and classifieds_obj.status=='D':
            signals.create_staffmail.send(sender=None,object=article_obj,module='articles',action='A',user=user)
        elif state=='Success': 
            signals.create_staffmail.send(sender=None,object=article_obj,module='articles',action='UG',user=user)
        
        if approval_settings.paid and state=='Success':
            article_obj.status='P'
            try:mail_publish_article(article_obj)
            except:pass
        else:article_obj.status='N'
        article_obj.save()
        signals.create_notification.send(sender=None,user=article_obj.created_by, obj=article_obj, not_type='submitted in',obj_title=article_obj.title)
        if payment_level=='FR':payment_level='Article Own Story'
        elif payment_level=='PR':payment_level='Article Pressrelease'
        elif payment_level=='A':payment_level='Article Advertorial'
        elif payment_level=='RR':payment_level='Article Review Request'
        object_name=article_obj.get_payment_title()
        
    elif model == 'event':
        approval_settings=ApprovalSettings.objects.get(name='events')
        ct = ContentType.objects.get_for_model(Event)
        event=Event.objects.get(pk=object_id)
        
        if state=='Success' and classifieds_obj.status=='D':
            signals.create_staffmail.send(sender=None,object=event,module='events',action='A',user=user)
        elif state=='Success': 
            signals.create_staffmail.send(sender=None,object=event,module='events',action='UG',user=user)
        
        if approval_settings.paid and state=='Success':
            event.status='P'
            try:mail_publish_event(event)
            except:pass
        else:event.status='N'
        event.payment = EventPrice.objects.get(level=payment_level)
        if str(payment_level)=='level2':
            event.listing_type='F'
            payment_level='Featured Event '
        elif str(payment_level)=='level1':
            event.listing_type='S'
            payment_level='Sponsored Event'
        event.listing_duration=gc_obj[7]
        try:
            sdate=gc_obj[5].split('/')
            edate=gc_obj[6].split('/')
            event.listing_start=datetime.datetime(int(sdate[0]),int(sdate[1]),int(sdate[2]))
            event.listing_end=datetime.datetime(int(edate[0]),int(edate[1]),int(edate[2]))
        except:
            sdate=gc_obj[5].split('-')
            edate=gc_obj[6].split('-')
            event.listing_start=datetime.datetime(int(sdate[0]),int(sdate[1]),int(sdate[2]))
            event.listing_end=datetime.datetime(int(edate[0]),int(edate[1]),int(edate[2]))
        event.listing_price=obj.order_total
        event.save()
        notifictn_type = 'added as '+event.payment.level_label.lower()+' in'
        signals.create_notification.send(sender=None,user=event.created_by, obj=event, not_type=notifictn_type,obj_title=event.title)
        start_date=event.listing_start
        end_date=event.listing_end
        object_name=event.get_payment_title()
        
    elif model == 'deal':
        ct = ContentType.objects.get_for_model(Deal)
        deal = Deal.objects.get(pk = object_id)
        deal_payment = DealPayment.objects.get(pk = payment_level)
        if state=='Success':
            deal_payment.status = 'S'
            deal_payment.is_paid = True
        elif status=='PAYMENT_DECLINED' or status=='CANCELLED' or status=='CANCELLED_BY_GOOGLE':
            deal_payment.status = 'E'
            deal_payment.is_paid = False
        else:
            deal_payment.status = 'W'
            deal_payment.is_paid = False

        deal_payment.transaction_no = obj.serial_number
        deal_payment.payment_status = status
        deal_payment.payer_status = status
        deal_payment.transaction_type ='GoogleCheckout'
        deal_payment.save()
        signals.create_notification.send(sender=None,user=deal_payment.created_by, obj=deal, not_type='bought as',obj_title=deal.title)
        payment_level='Purchased Deal(s)'
        if state=='Success':
            signals.create_staffmail.send(sender=None,object=deal,module='deals',action='P',user=user)
            if deal_payment.is_friend: 
                buy_success_gift_mail(deal_payment,deal)
                send_voucher_mail(deal_payment,deal,deal_payment.gift_addr.g_email)
            else:
                buy_success_mail(deal_payment,deal)
                send_voucher_mail(deal_payment,deal,deal_payment.email)
        object_name=deal.get_payment_title()
    
    elif model == 'shop':
        ct = ContentType.objects.get_for_model(Order)
        order_obj = Order.objects.get(pk=object_id) 
        
        order_obj.transaction_id = obj.serial_number
        if status=='PAYMENT_DECLINED' or status=='CANCELLED' or status=='CANCELLED_BY_GOOGLE':
            order_obj.state = 2
        elif status == 'CHARGED':
            order_obj.state = 1
            try:
                cart = Cart.objects.get(user_id=order_obj.user.id)
                cart.delete()
            except:pass 
            send_mail_order(order_obj)       
        else:
            order_obj.state = 4   
        
        order_obj.payment_method = 'GC'  
        order_obj.payment_price = obj.order_total
        order_obj.save() 
        send_notify(order_obj)
        
    po = PaymentOrder()
    po.content_type=ct
    po.object_id= object_id
    po.invoice_no=invoice
    po.transactionid=obj.serial_number
    po.txn_type="google_sub"
    po.payment_mode='Googlecheckout'
    po.amount=obj.order_total
    po.listing_type=payment_level
    po.user=user
    po.status=state
    if start_date:po.start_date=start_date
    if end_date:po.end_date=end_date 
    po.object_name=object_name
    po.save()

def update_order_gc_notification(sender,**kwargs):
    obj=kwargs['response']
    gc_obj=obj.cart_items
    gc_obj=gc_obj.split('#@#')[0]
    gc_obj=gc_obj.split(':#')
    model=gc_obj[0]
    object_id=gc_obj[1]
    invoice=gc_obj[2]
    payment_level=gc_obj[3]
    user=User.objects.get(pk=gc_obj[4])
    
    status=obj.financial_order_state
    if status=='CHARGED':state='Success'
    else:state='Pending'
    
    if model == 'classifieds':
        approval_settings=ApprovalSettings.objects.get(name='classifieds')
        ct = ContentType.objects.get_for_model(Classifieds)
        classifieds_obj=Classifieds.objects.get(pk=object_id)
        
        if approval_settings.paid and state=='Success':
            classifieds_obj.status='P'
            try:mail_publish_classifieds(classifieds_obj)
            except:pass
        else:classifieds_obj.status='N'

        classifieds_price_obj = ClassifiedPrice.objects.get(level =payment_level)
        period=classifieds_price_obj.contract_period

        classifieds_obj.payment=classifieds_price_obj
        if state=='Success':  
            classifieds_obj.listing_start_date=date.today()
            classifieds_obj.listing_end_date=date.today()+relativedelta(months=+period)

        classifieds_obj.price=obj.order_total
        if classifieds_price_obj.level=='level2':
            classifieds_obj.listing_type='F'
            payment_level='Featured Classified'
        elif classifieds_price_obj.level=='level1':
            classifieds_obj.listing_type='S'
            payment_level='Sponsored Classified'
        classifieds_obj.is_paid=True
        classifieds_obj.save()  
        start_date=classifieds_obj.listing_start_date
        end_date=classifieds_obj.listing_end_date
        
        if state=='Success' and classifieds_obj.status=='D':
            signals.create_staffmail.send(sender=None,object=classifieds_obj,module='classifieds',action='A',user=user)
        elif state=='Success': 
            signals.create_staffmail.send(sender=None,object=classifieds_obj,module='classifieds',action='UG',user=user)
    
    elif model == 'business':
        appreoval_settings = ApprovalSettings.objects.get(name='business')
        ct = ContentType.objects.get_for_model(Business)
        business_obj=Business.objects.get(pk=object_id)
        try:
            #############################CLAIM######################################
            if business_obj.is_claimable:
                save_to_claim_business(user,business_obj,True,True)
                signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='C',user=user)
            #############################CLAIM######################################
                claim=BusinessClaim.objects.get(business=business_obj)
                claimsettings=BusinessClaimSettings.get_setting()
                
                
                if claimsettings.auto_aprove_paid_buz_claim:
                    claim.is_approved=True
                    claim.save()
                    business_obj.created_by=claim.user
                    business_obj.status='P'
                    try:mail_publish_business(business_obj)
                    except:pass
                else:business_obj.status='N'
            else:
                if business_obj.status=='D':
                    signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='A',user=user)
                else:
                    signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='UG',user=user)
                if appreoval_settings.paid:
                    business_obj.status='P'
                    try:mail_publish_business(business_obj)
                    except:pass
                else:business_obj.status='N'
        except:
            if business_obj.status=='D':
                signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='A',user=user)
            else:
                signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='UG',user=user)
            if appreoval_settings.paid:
                business_obj.status='P'
                try:mail_publish_business(business_obj)
                except:pass
            else:business_obj.status='N'
       
        if state=='Success' and business_obj.is_claimable:
            buz_settings=BusinessClaimSettings.get_settings()
            if buz_settings.after_failed_payment=='B':business_obj.status='B'
            else:business_obj.featured_sponsored='B'
        else:business_obj.status='P'
        
        business_obj.sp_cost=obj.order_total
       
        business_price_obj = BusinessPrice.objects.get(level = payment_level)
        business_obj.payment=business_price_obj
        business_obj.lstart_date=date.today()
        if business_obj.payment_type == 'Y':business_obj.lend_date=date.today()+relativedelta(years=+1)
        else:business_obj.lend_date=date.today()+relativedelta(months=+1)
        
        if business_price_obj.level=='level2':
            business_obj.featured_sponsored='F'
            payment_level='Featured Business'
        elif business_price_obj.level=='level1':
            business_obj.featured_sponsored='S'
            payment_level='Sponsored Business'
        business_obj.is_paid=True
        business_obj.save()
        notifictn_type = 'listed as '+business_price_obj.level_label.lower()+' in'
        signals.create_notification.send(sender=None,user=business_obj.created_by, obj=business_obj, not_type=notifictn_type,obj_title=business_obj.name)  
        
        start_date=business_obj.lstart_date
        end_date=business_obj.lend_date
        object_name=business_obj.get_payment_title()
         
    elif model == 'article':
        approval_settings=ApprovalSettings.objects.get(name='article')
        ct = ContentType.objects.get_for_model(Article)
        article_obj=Article.objects.get(pk = object_id)
        if approval_settings.paid and state=='Success':
            article_obj.status='P'
            try:mail_publish_article(article_obj)
            except:pass
        else:article_obj.status='N'
        article_obj.save()
        
        if state=='Success' and classifieds_obj.status=='D':
            signals.create_staffmail.send(sender=None,object=article_obj,module='articles',action='A',user=user)
        elif state=='Success': 
            signals.create_staffmail.send(sender=None,object=article_obj,module='articles',action='UG',user=user)
        
    elif model == 'event':
        approval_settings=ApprovalSettings.objects.get(name='events')
        ct = ContentType.objects.get_for_model(Event)
        event=Event.objects.get(pk=object_id)
        if approval_settings.paid and state=='Success':
            event.status='P'
            try:mail_publish_event(event)
            except:pass
        else:event.status='N'
        event.save()
        
        if state=='Success' and classifieds_obj.status=='D':
            signals.create_staffmail.send(sender=None,object=event,module='events',action='A',user=user)
        elif state=='Success': 
            signals.create_staffmail.send(sender=None,object=event,module='events',action='UG',user=user)
            
    elif model == 'deal':
        ct = ContentType.objects.get_for_model(Deal)
        deal = Deal.objects.get(pk = object_id)
        deal_payment = DealPayment.objects.get(pk = payment_level)
        if state=='Success':
            deal_payment.status = 'S'
            deal_payment.is_paid = True
        elif status=='PAYMENT_DECLINED' or status=='CANCELLED' or status=='CANCELLED_BY_GOOGLE':
            deal_payment.status = 'E'
            deal_payment.is_paid = False
        else:
            deal_payment.status = 'W'
            deal_payment.is_paid = False
      
        deal_payment.transaction_no = obj.serial_number
        deal_payment.payment_status = status
        deal_payment.payer_status = status
        deal_payment.transaction_type ='GoogleCheckout'
        deal_payment.save()
        if state=='Success':
            signals.create_staffmail.send(sender=None,object=deal,module='deals',action='P',user=user)
            if deal_payment.is_friend: 
                buy_success_gift_mail(deal_payment,deal)
                send_voucher_mail(deal_payment,deal,deal_payment.gift_addr.g_email)
            else:
                buy_success_mail(deal_payment,deal)
                send_voucher_mail(deal_payment,deal,deal_payment.email)
    
    elif model == 'shop':
        ct = ContentType.objects.get_for_model(Order)
        order_obj = Order.objects.get(pk=object_id) 
        
        if status=='PAYMENT_DECLINED' or status=='CANCELLED' or status=='CANCELLED_BY_GOOGLE':
            order_obj.state = 2
        elif status == 'CHARGED':
            order_obj.state = 1
            try:
                cart = Cart.objects.get(user_id=order_obj.user.id)
                cart.delete()
            except:pass 
            send_mail_order(order_obj)       
        else:
            order_obj.state = 4   
        
        order_obj.payment_method = 'GC' 
        order_obj.save()
        send_notify(order_obj) 
    
                 
    po = PaymentOrder.objects.get(transactionid=obj.serial_number)
    po.txn_type="google_sub"
    po.status=state
    po.save()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
########################### Authorizenet ############################### 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  


def successfull_authnet_payment(sender,dicto,**kwargs):
    ath_obj = sender
    start_date=end_date=None
    object_name=''
    custom = dicto['custom'].split(":")
    module,obj_id,pay_level,user,duration,start_date,end_date  = dicto['custom'].split(':')
    try:user=User.objects.get(pk = int(user))
    except:user=None
    if module == 'shop':
        ct = ContentType.objects.get_for_model(Order)
        order_obj = Order.objects.get(pk = int(obj_id))
        oid = order_obj.id
        order_obj.transaction_id = ath_obj.trans_id
        if ath_obj.response_code == 4:
            order_obj.state = 4
        elif ath_obj.response_code == 2:
            order_obj.state = 2     
        elif ath_obj.response_code == 1:
            order_obj.state = 1
            try:
                cart = Cart.objects.get(user_id=order_obj.user.id)
                cart.delete()
            except:pass     
            send_mail_order(order_obj)  
        else:
            order_obj.state = 3   
        order_obj.payment_method = 'AN'
        order_obj.payment_price = ath_obj.amount
        order_obj.save()
        send_notify(order_obj)
        
    elif custom[0] == 'event':
        approval_settings=ApprovalSettings.objects.get(name='events')
        ct = ContentType.objects.get_for_model(Event)
        oid=int(custom[1])
        event=Event.objects.get(pk=oid)
        if event.status=='D':signals.create_staffmail.send(sender=None,object=event,module='events',action='A',user=user)
        else:signals.create_staffmail.send(sender=None,object=event,module='events',action='UG',user=user)
        if approval_settings.paid and int(ath_obj.response_code) == 1:
            event.status='P'
            try:mail_publish_event(event)
            except:pass
        else:event.status='N'
        
        try:
            event_price_obj = EventPrice.objects.get(level=str(custom[2]))
            event.payment=event_price_obj
        except:pass
        if str(custom[2])=='level2':
            event.listing_type='F'
            custom[2]='Featured Event '
        elif str(custom[2])=='level1':
            event.listing_type='S'
            custom[2]='Sponsored Event'
        event.listing_duration=custom[4]
        try:
            sdate=custom[5].split('/')
            edate=custom[6].split('/')
            event.listing_start=datetime.datetime(int(sdate[0]),int(sdate[1]),int(sdate[2]))
            event.listing_end=datetime.datetime(int(edate[0]),int(edate[1]),int(edate[2]))
        except:
            sdate=custom[5].split('-')
            edate=custom[6].split('-')
            event.listing_start=datetime.datetime(int(sdate[0]),int(sdate[1]),int(sdate[2]))
            event.listing_end=datetime.datetime(int(edate[0]),int(edate[1]),int(edate[2]))
        event.listing_price=ath_obj.amount
        event.save()
        notifictn_type = 'listed as '+event_price_obj.level_label.lower()+' in'
        signals.create_notification.send(sender=None,user=event.created_by, obj=event, not_type=notifictn_type,obj_title=event.title)    
        start_date=event.listing_start
        end_date=event.listing_end
        object_name=event.get_payment_title()
    
    elif custom[0] == 'banners':
        approval_settings=ApprovalSettings.objects.get(name='banners')
        ct = ContentType.objects.get_for_model(BannerAdvertisements)
        oid=int(custom[1])
        banner_obj=BannerAdvertisements.objects.get(pk=oid)
        total_amount = banner_obj.total_amount
        if banner_obj.status=='D':signals.create_staffmail.send(sender=None,object=banner_obj,module='banners',action='A',user=user)
        else:signals.create_staffmail.send(sender=None,object=banner_obj,module='banners',action='UG',user=user)
        if approval_settings.paid and int(ath_obj.response_code) == 1:
            banner_obj.status='P'
            try:mail_publish_banner(banner_obj)
            except:pass
        else:banner_obj.status='N'
        
        try:
            banner_price_obj = BannerPayment.objects.get(level=str(custom[2]))
            banner_obj.payment=banner_price_obj
        except:pass
        banner_obj.total_amount=float(banner_obj.total_amount)
        banner_obj.save()
        notifictn_type = 'listed as '+banner_price_obj.level_label.lower()+' in'
        signals.create_notification.send(sender=None,user=banner_obj.created_by, obj=banner_obj, not_type=notifictn_type,obj_title=banner_obj.title)    
        object_name=banner_obj.get_payment_title()
        
    elif custom[0] == 'classifieds':
        approval_settings=ApprovalSettings.objects.get(name='classifieds')
        ct = ContentType.objects.get_for_model(Classifieds)
        oid = custom[1]
        classifieds_obj=Classifieds.objects.get(pk=oid)
        
        if classifieds_obj.status=='D':signals.create_staffmail.send(sender=None,object=classifieds_obj,module='classifieds',action='A',user=user)
        else:signals.create_staffmail.send(sender=None,object=classifieds_obj,module='classifieds',action='UG',user=user)
        
        if approval_settings.paid and int(ath_obj.response_code) == 1:
            classifieds_obj.status='P'
            try:mail_publish_classifieds(classifieds_obj)
            except:pass
        else:classifieds_obj.status='N'

        classifieds_price_obj = ClassifiedPrice.objects.get(level =str(custom[2]))
        period=classifieds_price_obj.contract_period
        
        classifieds_obj.payment=classifieds_price_obj
        classifieds_obj.listing_start_date=date.today()
        classifieds_obj.listing_end_date=date.today()+relativedelta(months=+period)
        
        classifieds_obj.price=ath_obj.amount
        if classifieds_price_obj.level=='level2':
            classifieds_obj.listing_type='F'
            custom[2]='Featured Classified'
        elif classifieds_price_obj.level=='level1':
            classifieds_obj.listing_type='S'
            custom[2]='Sponsored Classified'
        classifieds_obj.is_paid=True
        classifieds_obj.save()  
        notifictn_type = 'posted as '+classifieds_price_obj.level_label.lower()+' in'
        signals.create_notification.send(sender=None,user=classifieds_obj.created_by, obj=classifieds_obj, not_type=notifictn_type,obj_title=classifieds_obj.title) 
        start_date=classifieds_obj.listing_start_date
        end_date=classifieds_obj.listing_end_date
        object_name=classifieds_obj.get_payment_title()
    
    elif custom[0] == 'article':
        approval_settings=ApprovalSettings.objects.get(name='article')
        ct = ContentType.objects.get_for_model(Article)
        oid = custom[1]
        article_obj=Article.objects.get(pk = oid)
        if approval_settings.paid and int(ath_obj.response_code) == 1:
            article_obj.status='P'
            try:mail_publish_article(article_obj)
            except:pass
        else:article_obj.status='N'
        article_obj.save()
        signals.create_notification.send(sender=None,user=article_obj.created_by, obj=article_obj, not_type='submitted in',obj_title=article_obj.title)
        signals.create_staffmail.send(sender=None,object=article_obj,module='articles',action='A',user=user)
        if custom[2]=='FR':custom[2]='Article Own Story'
        elif custom[2]=='PR':custom[2]='Article Pressrelease'
        elif custom[2]=='A':custom[2]='Article Advertorial'
        elif custom[2]=='RR':custom[2]='Article Review Request'
        object_name=article_obj.get_payment_title()
    
    elif custom[0] == 'deal':
        ct = ContentType.objects.get_for_model(Deal)
        oid = custom[1]
        deal = Deal.objects.get(pk = oid)
        deal_payment = DealPayment.objects.get(pk = custom[2])
        deal_payment.status = 'S'
            
        deal_payment.transaction_no = ath_obj.invoice_num
        deal_payment.is_paid = True
        if int(ath_obj.response_code) == 1:
            deal_payment.payment_status = 'Success'
            deal_payment.payer_status = 'Success'
        else:
            deal_payment.payment_status = 'Pending'
            deal_payment.payer_status = 'Pending'
        deal_payment.transaction_type = ath_obj.type
        deal_payment.save()
        user=deal_payment.created_by
        signals.create_notification.send(sender=None,user=deal_payment.created_by, obj=deal, not_type='bought as',obj_title=deal.title) 
        signals.create_staffmail.send(sender=None,object=deal,module='deals',action='P',user=user)
        custom[2]='Purchased Deal(s)'
        if deal_payment.is_friend: 
            buy_success_gift_mail(deal_payment,deal)
            send_voucher_mail(deal_payment,deal,deal_payment.gift_addr.g_email)
        else:
            buy_success_mail(deal_payment,deal)
            send_voucher_mail(deal_payment,deal,deal_payment.email)
        object_name=deal.get_payment_title()
    
    try:po = PaymentOrder.objects.get(invoice_no = ath_obj.invoice)
    except:po = PaymentOrder()
    po.content_type = ct
    po.object_id = oid
    try:po.invoice_no = ath_obj.invoice_num
    except:po.invoice_no = ath_obj.invoice
    po.transactionid = ath_obj.trans_id
    po.txn_type = ath_obj.type
    po.payment_mode='Authorize.net'
    po.amount=ath_obj.amount
    po.user = user
    try:
        if ath_obj.response_code == 1 or ath_obj.response_code == '1':
            po.status='Success'
        else:
            po.status='Pending'
    except:
        try:
            if pdt_obj.response_code == 1:
                po.status='Success'
            else:
                po.status='Pending'
        except:po.status='Pending'
    po.object_name="Shop Item:"+str(ath_obj.invoice_num)
    po.save()
    
def flagged_authnet_payment(sender,dicto,**kwargs):
    ath_obj = sender
    ### Do Smothing ####

            
pdt_successful.connect(update_order)  

payment_was_successful.connect(update_order)
payment_was_updated.connect(update_order_notification)

transaction_was_successful.connect(update_order_gc)  
transactionnotification_was_successful.connect(update_order_gc_notification)


auth_net.payment_was_successful.connect(successfull_authnet_payment)
auth_net.payment_was_flagged.connect(successfull_authnet_payment)
