from datetime import timedelta
import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from common.mail_utils import mail_publish_banner
import json
import stripe
from time import strptime
import time

from article.models import Article, ArticlePrice
from banners.models import BannerAdvertisements, BannerPayment
from business.models import Business, BusinessPrice, BusinessClaim, \
    BusinessClaimSettings
from business.utils import save_to_claim_business
from classifieds.models import Classifieds, ClassifiedPrice
from common import signals
from common.mail_utils import mail_publish_classifieds, mail_publish_business, \
    mail_publish_event, mail_publish_article
from common.models import *
from common.staff_messages import BANNER_MSG
from common.static_msg import PAYMNET_MSG
from common.user_messages import ARTICLE_MSG, EVENT_MSG, CLASSIFIED_MSG, \
    BUSINESS_MSG
from common.utils import get_global_settings
from deal.models import Deal, DealPayment
from deal.utils import buy_success_mail, send_voucher_mail, \
    buy_success_gift_mail
from events.models import Event, EventPrice
from payments.authorizenet import AUTHNET_POST_URL, AUTHNET_TEST_POST_URL
from payments.authorizenet.forms import SIMPaymentForm
from payments.authorizenet.utils import get_fingerprint
from payments.googlecheckout.views import GoogleCheckoutIntegration
from payments.models import PaymentOrder, OfflinePayment
from payments.stripes.models import StripePaymentDetails, StripePlanDetails
from payments.utils import *


#from payments.googlecheckout.models import GCNewOrderNotification
User = get_user_model()

@require_POST
@csrf_exempt
def stripe_notify(request):
    try:
        currency=PaymentConfigure.get_payment_settings()
        stripe.api_key = currency.stripe_private_key
        json_obj = json.loads(request.body)
        if json_obj['type']=='charge.succeeded':
            try:
                po=PaymentOrder.objects.get(transactionid=json_obj['id'])
                po.status='Success'
                po.save()
            except:pass
        elif json_obj['type']=='charge.failed':
            try:
                po=PaymentOrder.objects.get(transactionid=json_obj['id'])
                po.status='Failed'
                po.save()
            except:pass
        elif json_obj['type']=='invoice.payment_failed':
            try:
                spd=StripePaymentDetails.objects.get(customer_id=json_obj['data']['object']['customer'])
                business=Business.objects.get(id=spd.content_object.id)
                business.status='N'
                business.save()
            except:pass
        elif json_obj['type']=='invoice.payment_succeeded':
            try:spd=StripePaymentDetails.objects.get(customer_id=json_obj['data']['object']['customer'])
            except:spd=False
            if spd and spd.module=='Business':
                plan_id=json_obj['data']['object']['lines']['data'][0]['plan']['id']
                subscription_id=json_obj['data']['object']['lines']['data'][0]['id']
                plan=plan_id.split('_')
                sp_cost=plan[3]
                if plan[2].upper()=='MONTH':payment_type='M'
                else:payment_type='Y'
                if plan[1]=='Sponsored':level='level1'
                else:level='level2'
                business_price_obj=BusinessPrice.objects.get(level=level)
                
                business_obj=spd.content_object
                try:po=PaymentOrder.objects.get(transactionid=subscription_id)
                except:po=PaymentOrder(content_object=business_obj)
                po.invoice_no=get_invoice_num()
                po.transactionid=subscription_id
                po.txn_type=''
                po.payment_mode='Stripe'
                po.status='Success'
                appreoval_settings = ApprovalSettings.objects.get(name='business')
                
                try:
                    #############################CLAIM######################################
                    if business_obj.is_claimable:
                        save_to_claim_business(request.user,business_obj,approve=True,paid=True)
                        signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='C',user=spd.user)
                    #############################CLAIM######################################
                        claim=BusinessClaim.objects.get(business=business_obj)
                        if business_obj.status == 'P':
                            try:mail_publish_business(business_obj)
                            except:pass
                    else:
                        if business_obj.status=='D':
                            signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='A',user=spd.user)
                        else:
                            signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='UG',user=spd.user)
                        if appreoval_settings.paid:
                            business_obj.status='P'
                            try:mail_publish_business(business_obj)
                            except:pass
                        else:business_obj.status='N'
                except:
                    if business_obj.status=='D':
                        signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='A',user=spd.user)
                    else:
                        signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='UG',user=spd.user)
                    if appreoval_settings.paid:
                        business_obj.status='P'
                        try:mail_publish_business(business_obj)
                        except:pass
                    else:business_obj.status='N'
                    
                business_obj.sp_cost=float(sp_cost)
               
                business_obj.payment=business_price_obj
                business_obj.lstart_date=datetime.datetime.today()
                if payment_type == 'Y':business_obj.lend_date=datetime.datetime.today()+relativedelta(years=+1)
                else:business_obj.lend_date=datetime.datetime.today()+relativedelta(months=+1)
                
                if business_price_obj.level=='level2':
                    business_obj.featured_sponsored='F'
                    business_price_obj_level='Featured Business'
                elif business_price_obj.level=='level1':
                    business_obj.featured_sponsored='S'
                    business_price_obj_level='Sponsored Business'
                business_obj.is_paid=True
                business_obj.save()
                notifictn_type = 'listed as '+business_price_obj.level_label.lower()+' in'
                signals.create_notification.send(sender=None,user=business_obj.created_by, obj=business_obj, not_type=notifictn_type,obj_title=business_obj.name)  
                    
                po.amount=float(sp_cost)
                po.start_date = business_obj.lstart_date
                po.end_date =business_obj.lend_date
                po.user = spd.user
                po.listing_type =business_price_obj_level
                po.object_name=business_obj.get_payment_title() 
                po.save()
        return HttpResponse('success')
    except:
        return HttpResponse(status=500)


def get_stripe_plan_object(interval, amount):
    if amount == 0:
        return None
    currency = PaymentConfigure.get_payment_settings()
    stripe.api_key = currency.stripe_private_key
    try:
        live = stripe.Plan.retrieve("%0.2f-%s-plan" % (amount, interval))
    except:
        live = stripe.Plan.create(
            amount=int(amount*100), 
            interval=interval, 
            name="%0.2f %s plan" % (amount, interval), 
            currency='usd', 
            id="%0.2f-%s-plan" % (amount, interval)
        )
    try:
        plan = StripePlanDetails.objects.get(interval=interval,amount=amount,status='A')
    except:
        plan = StripePlanDetails(
            name="%0.2f %s plan" % (amount, interval),
            plan_id="%0.2f-%s-plan" % (amount, interval),
            currency="usd",
            amount=amount,
            interval =interval,
            type="%s_plan"%(interval),
            status = "A"
        )
        plan.save()
    return plan
        
@login_required 
def business_payments_confirm(request,bid,lid):
    try:
        claim=request.REQUEST['c']
        business_obj = Business.objects.get(id=bid)
        if claim == '1' and not business_obj.is_claimable:
            return HttpResponseRedirect(reverse('user_manage_business')+'?msg=OOPS&mtype=e')
        claim=1
    except:
        claim=0
        business_obj = Business.objects.get(id=bid,created_by=request.user)
    payment_type = request.REQUEST['type']
    if payment_type not in ['Y','M']:
        return HttpResponseRedirect(reverse('user_manage_business')+'?msg=OOPS&mtype=e')
    business_price_obj = BusinessPrice.objects.get(id=lid)
    level = business_price_obj.level
    
    sp_cost=0
    if payment_type=='M':
        if business_price_obj.level=='level1':
            for b_c in business_obj.categories.all():
                if b_c.price_month:
                    sp_cost=sp_cost+b_c.price_month
                else:
                    if b_c.parent_cat.price_month:
                        sp_cost=sp_cost+b_c.parent_cat.price_month
        elif business_price_obj.level=='level2':
            sp_cost=business_price_obj.price_month
           
    elif payment_type=='Y': 
        if business_price_obj.level=='level1':
            for b_c in business_obj.categories.all():
                if b_c.price_year:
                    sp_cost=sp_cost+b_c.price_year
                else:
                    if b_c.parent_cat.price_year:
                        sp_cost=sp_cost+b_c.parent_cat.price_year
        elif business_price_obj.level=='level2':
            sp_cost=business_price_obj.price_year
    
    
    
    lstart_date = datetime.datetime.now()
    if payment_type == 'Y':
        lend_date = datetime.date.today()+relativedelta(years=+1)
    else:
        lend_date = datetime.date.today()+relativedelta(months=+1)
    if business_price_obj.level != 'level0':
        data = {'claim':claim, 'pay_obj':business_obj, 'level': business_price_obj, 'listing_price': sp_cost, 'listing_period': payment_type, 'lstart_date': lstart_date, 'lend_date': lend_date, 'stripe_sp_cost': int(sp_cost * 1000) / 10}
        data['payment_config']=currency=PaymentConfigure.get_payment_settings()
        if request.method=='POST':
            stripe_token = request.POST.get('stripeToken',False)
            if stripe_token:
                currency = PaymentConfigure.get_payment_settings()
                stripe.api_key = currency.stripe_private_key
                globalsettings=get_global_settings()
                po=PaymentOrder(content_object=business_obj)
                approval_settings=ApprovalSettings.objects.get(name='business')
                if business_price_obj.level=='level2':
                    fs = 'F'
                elif business_price_obj.level=='level1':
                    fs = 'S'
                
                if currency.allow_subscription:
                    #############################STRIPE SUBSCRIPTION############################
                    period = request.POST.get('stripePeriod')
                    stripe_plan = get_stripe_plan_object(interval=period,amount=sp_cost)
                    plan_id = stripe_plan.plan_id
                    customer = stripe.Customer.create(
                        card = stripe_token,
                        description="%s - (%s) " % (business_obj.name, request.user.email)
                    )
                    subscription = customer.subscriptions.create(plan=plan_id)
                    customer.email = customer.cards.data[0].name
                    customer.save()
                    if subscription.status == "active":
                        business_obj.is_paid = True
                        business_obj.sp_cost = sp_cost
                        
                        po.status='Success'
                        po.transactionid = customer.subscription.id
                        
                        spd = StripePaymentDetails()
                        spd.user = request.user
                        spd.object_id = business_obj.id
                        spd.customer_id = customer.id
                        spd.plan_id = stripe_plan
                        spd.module = 'business'
                        spd.subscription_id = customer.subscription.id
                        spd.email_id = customer.email
                        spd.content_object = business_obj
                        spd.subscription_status = customer.subscription.status
                        spd.save()
                        
                        if business_obj.status=='D':
                            signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='A',user=request.user)
                        else:
                            signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='UG',user=request.user)
                        notifictn_type = 'listed as '+business_price_obj.level_label.lower()+' in'
                        signals.create_notification.send(sender=None,user=request.user, obj=business_obj, not_type=notifictn_type,obj_title=business_obj.name)
                        business_obj.featured_sponsored = fs
                        if approval_settings.paid:
                            business_obj.status='P'
                            try:mail_publish_business(business_obj)
                            except:pass
                    else:
                        business_obj.status='N'
                        po.status='Failed'
                    business_obj.save()
                    #############################STRIPE SUBSCRIPTION############################
                else:
                    #############################STRIPE ONE TIME PAYMENT############################
                    charge = stripe.Charge.create(amount=int(sp_cost*100),currency=currency.currency_code,card=stripe_token,description=request.user.email)
                    if charge.paid:
                        po.status='Success'
                        po.transactionid=charge.id
                        business_obj.featured_sponsored=fs
                        approval_settings=ApprovalSettings.objects.get(name='business')
                        if business_obj.status=='D':signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='A',user=request.user)
                        else:signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='UG',user=request.user)
                        if approval_settings.paid:
                            business_obj.status='P'
                            try:mail_publish_business(business_obj)
                            except:pass
                        else:business_obj.status='N'
                    else:po.status='Failed'
                    #############################STRIPE ONE TIME PAYMENT############################
                    
                if claim:
                    claim_setting = BusinessClaimSettings.get_setting()
                    if ( claim_setting.auto_aprove_paid_buz_claim and business_obj.featured_sponsored in ['F', 'S'] ) or \
                        ( claim_setting.auto_aprove_free_buz_claim and business_obj.featured_sponsored == 'B' ):
                        save_to_claim_business(business=business_obj, approve=True, paid=True)
                    else:
                        save_to_claim_business(business=business_obj, approve=False, paid=True)
                    if business_obj.status == 'P':
                        try:mail_publish_business(business_obj)
                        except:pass
                    signals.create_staffmail.send(sender=None,object=business_obj,module='business',action='C',user=request.user)
                
                
                business_obj.total_amount=float(sp_cost)
                business_obj.save() 
                po.invoice_no=get_invoice_num()
                po.txn_type=''
                po.payment_mode='Stripe'
                po.amount=float(sp_cost)
                po.user = request.user
                if business_price_obj:po.listing_type =str(business_price_obj.level_label)+" Business"
                else:po.listing_type =str(business_obj.get_payment_listing_type())+" Business"
                po.object_name=business_obj.name
                po.save()
                #return HttpResponseRedirect("/user/payments/?msg=REV&mtype=s")
                return HttpResponseRedirect(reverse("payments_success", args=["business"]))
                try:
                    ""
                except:
                    data['msg']=PAYMNET_MSG['OOPS']
                    data['mtype']='alert-error'
            else:
                form = get_recurring_payment_form(business_obj.name,sp_cost,payment_type,':'.join(['business',str(business_obj.id),str(business_price_obj.level),str(request.user.id),str(claim)]))
                data = {'form':form,'module':'business'}
                return render_to_response("payments/conformation/paypal_submit.html", data, context_instance=RequestContext(request))
            
        #################Google Checkout #######################
        if payment_type=='Y':payment_type='YEARLY'
        else:payment_type='MONTHLY'
        globalsettings=get_global_settings()
        c_msg="business:#"+str(business_obj.id)+':#'+str(get_invoice_num())+':#'+business_price_obj.level+':#'+str(request.user.id)
        fields = {'items': [{'amount':sp_cost,
                             'name': business_obj.name,
                             'description':str(business_price_obj.level_label)+" Business",
                             'id': c_msg,
                             'currency':currency.currency_code,
                             'quantity': 1,
                             'listing_period':payment_type,
                            }],
                  'return_url': "%s/user/payments/?msg=REV&mtype=s"%(globalsettings.website_url),}
        details={
            'merchant_id':str(currency.merchant_id),
            'merchant_key':str(currency.merchant_key)
        }
        google_checkout_obj=GoogleCheckoutIntegration(details)
        google_checkout_obj.add_fields(fields)
        data['gc_obj']= google_checkout_obj
        data['gc_payment_option']=google_checkout_obj.subs_generate_cart_xml
        #################Google Checkout #######################
        
        return render_to_response("payments/conformation/business.html", data, context_instance=RequestContext(request))
    return HttpResponseRedirect(reverse('user_manage_business')+'?msg=OOPS&mtype=e')

@login_required 
def banners_payments_confirm(request,bid,lid):
    data={}
    currency = PaymentConfigure.get_payment_settings()
    try:
        banner_obj = BannerAdvertisements.objects.get(id=bid,created_by=request.user)
        banner_price_obj = BannerPayment.objects.get(id=lid)
        vv = ContentType.objects.get_for_model(banner_obj)
        total_amounts = banner_obj.temp_amount
        try:
            paid_banner = PaymentOrder.objects.filter(content_type=vv,object_id = banner_obj.id).reverse()
            tot = 0
            for bans in paid_banner:
                tot = tot+bans.amount
            sp_cost = banner_obj.temp_amount-tot
            
            if sp_cost<1:
                sp_cost=1
        except:
            sp_cost=banner_obj.temp_amount
            
        if request.method=='POST':
            payment_settings=currency
            stripe_token = request.POST.get('stripeToken',False)
            if stripe_token:
                stripe.api_key = currency.stripe_private_key
                try:
                    charge = stripe.Charge.create(
                        amount=int(sp_cost*100), # amount in cents, again
                        currency=currency.currency_code,
                        card=stripe_token,
                        description=request.user.email
                    )
                    po=PaymentOrder(content_object=banner_obj)
                     
                    po.invoice_no=get_invoice_num()
                    po.transactionid=charge.id
                    po.txn_type=''
                    po.payment_mode='Stripe'
                    if charge.paid:
                        po.status='Success'
                        
                        approval_settings=ApprovalSettings.objects.get(name='banners')
                        if banner_obj.status=='D':
                            signals.create_staffmail.send(sender=None,object=banner_obj,module='banners',action='A',user=request.user)
                            if approval_settings.paid:
                                banner_obj.status='P'
                                try:mail_publish_banner(banner_obj)
                                except:pass
                            else:banner_obj.status='N'
                        else:
                            signals.create_staffmail.send(sender=None,object=banner_obj,module='banners',action='U',user=request.user)
                            if approval_settings.paid_update and banner_obj.status=='P':
                                banner_obj.status='P'
                                try:mail_publish_banner(banner_obj)
                                except:pass
                            else:banner_obj.status='N'
                        
                        banner_obj.impressions=banner_obj.temp_impressions
                        banner_obj.total_amount=float(total_amounts)
                        banner_obj.is_paid = True
                        banner_obj.save() 
                    else:po.status='Failed'  
                    po.amount=float(sp_cost)
                    po.user = request.user
                    if banner_price_obj:po.listing_type =str(banner_price_obj.level)+" Banners"
                    else:po.listing_type =str(banner_obj.get_payment_listing_type())+" Banners"
                    po.object_name=banner_obj.caption
                    po.save()
                    return HttpResponseRedirect("/user/payments/?msg=REV&mtype=s")
                except:
                    data['msg']=PAYMNET_MSG['OOPS']
                    data['mtype']='alert-error'
            else:
                payment_method = request.POST['payment_options']
                if 'paypal' in payment_method:
                    form = get_payment_form(banner_obj.caption,sp_cost,':'.join(['banners',str(banner_obj.id),str(banner_price_obj.level),str(request.user.id)]))
                    data = {'form':form,'module':'banners'}
                    return render_to_response("payments/conformation/paypal_submit.html", data, context_instance=RequestContext(request))
                elif 'authorizenet' in payment_method:
                    dates = datetime.datetime.now()
                    invoice_id='%s%s%s%s' % (dates.month, dates.day,dates.second,dates.microsecond,)+str(request.user.id)+str(banner_obj.id)
                    global_settings=CommonConfigure.objects.only('website_url')[:1][0]
                    params = {
                        'custom': ':'.join(['banners',str(banner_obj.id),str(banner_price_obj.level),str(request.user.id)]),
                        'x_amount': "%.2f" % float(sp_cost),
                        'x_fp_sequence': invoice_id,
                        'x_invoice_num': invoice_id,
                        'x_description': "Items Order Id:"+banner_obj.caption ,
                        'x_currency_code':payment_settings.currency_code,
                        'x_fp_timestamp': str(int(time.time())),
                        'x_receipt_link_url': global_settings.website_url+"/user/payments/msg=REV&mtype=i",
                        'x_relay_response':False,
                        }
                    
                    params['x_fp_hash'] = get_fingerprint(invoice_id,params['x_fp_timestamp'],params['x_amount'])
                    forms = SIMPaymentForm(initial=params)
                    
                    if settings.DEBUG:post_url = AUTHNET_TEST_POST_URL
                    else:post_url = AUTHNET_POST_URL
                    
                    data={}
                    data['forms']=forms
                    data['post_url']=post_url
                    data['module']='events'
                    return render_to_response("payments/conformation/authorize_submit.html", data, context_instance=RequestContext(request))
        data ={'pay_obj':banner_obj,'level':banner_price_obj,'listing_price':sp_cost}
        data['payment_config']=currency=PaymentConfigure.get_payment_settings()
        data['stripe_sp_cost']=float(sp_cost*100)
        return render_to_response("payments/conformation/banner.html", data, context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect('/user/banners/?msg=OOPS&mtype=e')


@login_required 
def event_payments_confirm(request,eid,lid):
    data={}
    currency = PaymentConfigure.get_payment_settings()
    try:
        event_obj = Event.objects.get(id=eid,created_by=request.user)
        event_price_obj = EventPrice.objects.get(id=lid)
        event_obj.payment = event_price_obj
        event_obj.save()
        c_type = ContentType.objects.get(model='event')
        OfflinePayment.objects.filter(content_type=c_type, object_id=event_obj.id, status='N').update(status='D')    
        if event_price_obj.level!='level0':
            try:
                sdate = datetime.datetime(*strptime(request.REQUEST["sdate"],"%m/%d/%Y")[0:5])
                edate = datetime.datetime(*strptime(request.REQUEST["edate"],"%m/%d/%Y")[0:5])
            except:
                sdate = datetime.datetime(*strptime(request.REQUEST["sdate"],"%m-%d-%Y")[0:5])
                edate = datetime.datetime(*strptime(request.REQUEST["edate"],"%m-%d-%Y")[0:5])
            duration=(edate-sdate)+ timedelta(days=1)
            cduration=int("%d" % duration.days)
            if event_price_obj.level=='level2':sp_cost=(float(event_price_obj.price)*cduration)
            else:sp_cost=event_price_obj.price
            
            duration=str(duration).split(',')
            duration=duration[0]
           
            if request.method=='POST':
                payment_settings=currency=PaymentConfigure.get_payment_settings()
                stripe_token = request.POST.get('stripeToken',False)
                if stripe_token:
                    stripe.api_key = currency.stripe_private_key
                    globalsettings=get_global_settings()
                    try:
                        charge = stripe.Charge.create(
                            amount=int(sp_cost*100), # amount in cents, again
                            currency=currency.currency_code,
                            card=stripe_token,
                            description=request.user.email
                        )
                        po=PaymentOrder(content_object=event_obj)
                         
                        po.invoice_no=get_invoice_num()
                        po.transactionid=charge.id
                        po.txn_type=''
                        po.payment_mode='Stripe'
                        if charge.paid:
                            po.status='Success'
                            event_obj.is_paid = True
                            approval_settings=ApprovalSettings.objects.get(name='events')
                            if event_obj.status=='D':
                                signals.create_staffmail.send(sender=None,object=event_obj,module='events',action='A',user=request.user)
                            else:
                                signals.create_staffmail.send(sender=None,object=event_obj,module='events',action='UG',user=request.user)
                            if approval_settings.paid:
                                event_obj.status='P'
                                try:mail_publish_event(event_obj)
                                except:pass
                            else:
                                event_obj.status='N'
                            
                            if event_price_obj.level=='level2':
                                event_obj.listing_type='F'
                            elif event_price_obj.level=='level1':
                                event_obj.listing_type='S'
                            event_obj.listing_duration=duration
                            event_obj.listing_start=sdate
                            event_obj.listing_end=edate
                            event_obj.listing_price=float(sp_cost)
                            event_obj.save() 
                        else:po.status='Failed'  
                        po.amount=float(sp_cost)
                        po.start_date = event_obj.listing_start
                        po.end_date =event_obj.listing_end
                        po.user = request.user
                        if event_price_obj:po.listing_type =str(event_price_obj.level_label)+" Event"
                        else:po.listing_type =str(event_obj.get_payment_listing_type())+" Event"
                        po.object_name=event_obj.title
                        po.save()
                        return HttpResponseRedirect(reverse("payments_success", args=["events"]))
                        #return HttpResponseRedirect("/user/payments/?msg=REV&mtype=s")
                    except:
                        data['msg']=PAYMNET_MSG['OOPS']
                        data['mtype']='alert-error'
                else:
                    payment_method = request.POST['payment_options']
                    if 'paypal' in payment_method:
                        
                        form = get_payment_form(
                            item_name=event_obj.title,
                            price=sp_cost,
                            custom=':'.join(['event',str(event_obj.id),
                                str(event_price_obj.level),
                                str(request.user.id),
                                str(duration),
                                str(request.REQUEST["sdate"]),
                                str(request.REQUEST["edate"])
                            ]),
                            module='events'
                        )
                        data = {'form':form,'module':'events'}
                        return render_to_response("payments/conformation/paypal_submit.html", data, context_instance=RequestContext(request))
                    elif 'authorize' in payment_method:
                        dates = datetime.datetime.now()
                        invoice_id='%s%s%s%s' % (dates.month, dates.day,dates.second,dates.microsecond,)+str(request.user.id)+str(event_obj.id)
                        global_settings=CommonConfigure.objects.only('website_url')[:1][0]
                        params = {
                            'custom': ':'.join(['event',str(event_obj.id),str(event_price_obj.level),str(request.user.id),str(duration),str(request.REQUEST["sdate"]),str(request.REQUEST["edate"])]),
                            'x_amount': "%.2f" % float(sp_cost),
                            'x_fp_sequence': invoice_id,
                            'x_invoice_num': invoice_id,
                            'x_description': "Items Order Id:"+event_obj.title ,
                            'x_currency_code':payment_settings.currency_code,
                            'x_fp_timestamp': str(int(time.time())),
                            'x_receipt_link_url': global_settings.website_url+"/user/payments/msg=REV&mtype=i",
                            'x_relay_response':False,
                            }
                        
                        params['x_fp_hash'] = get_fingerprint(invoice_id,params['x_fp_timestamp'],params['x_amount'])
                        forms = SIMPaymentForm(initial=params)
                        
                        if settings.DEBUG:post_url = AUTHNET_TEST_POST_URL
                        else:post_url = AUTHNET_POST_URL
                        data['forms']=forms
                        data['post_url']=post_url
                        data['module']='events'
                        return render_to_response("payments/conformation/authorize_submit.html", data, context_instance=RequestContext(request))

            data ={'pay_obj':event_obj,'level':event_price_obj,'listing_price':sp_cost,'listing_period':duration,'listing_start':sdate,'listing_end':edate}
            data['payment_config']=currency=PaymentConfigure.get_payment_settings()
            data['stripe_sp_cost']=float(sp_cost*100)
            #################Google Checkout #######################
            object_id=str(event_obj.id)
            invoice_id=str(get_invoice_num())
            listing_type=str(event_price_obj.level)
            user_id=str(request.user.id)
            globalsettings=get_global_settings()
            
            c_msg="event:#"+object_id+':#'+invoice_id+':#'+listing_type+':#'+user_id+":#"+str(request.REQUEST["sdate"])+":#"+str(request.REQUEST["edate"])+":#"+str(duration)
            fields = {'items': [{'amount':sp_cost,
                                 'name': event_obj.title,
                                 'description':str(event_price_obj.level_label)+" events for "+str(duration),
                                 'id': c_msg,
                                 'currency':currency.currency_code,
                                 'quantity': 1,
                                }],
                      'return_url': "%s/user/payments/?msg=REV&mtype=s"%(globalsettings.website_url),}
            
            details={'merchant_id':str(currency.merchant_id),'merchant_key':str(currency.merchant_key)}
            google_checkout_obj=GoogleCheckoutIntegration(details)
            google_checkout_obj.add_fields(fields)
            data['gc_obj']= google_checkout_obj
            data['gc_payment_option']=google_checkout_obj.generate_cart_xml
            #################Google Checkout #######################
            return render_to_response("payments/conformation/events.html", data, context_instance=RequestContext(request))
        return HttpResponseRedirect('/user/events/?msg=OOPS&mtype=e')
    except:
        return HttpResponseRedirect('/user/events/?msg=OOPS&mtype=e')

@login_required 
def classifieds_payments_confirm(request,cid,lid):
    try:
        currency = PaymentConfigure.get_payment_settings()
        classified_obj = Classifieds.objects.get(id = cid,created_by=request.user)
        classifieds_price_obj=ClassifiedPrice.objects.get(id = lid)
        period=classifieds_price_obj.contract_period
        
        listing_start_date=datetime.datetime.now()
        listing_end_date=datetime.date.today()+relativedelta(months=+period)
        sp_cost=0
        if classifieds_price_obj.level!='level0':
            if classifieds_price_obj.level == 'level1':
                if classified_obj.category.sp_price:sp_cost=classified_obj.category.sp_price
                else:sp_cost=classified_obj.category.parent.sp_price
            else:sp_cost=classifieds_price_obj.price
            duration=str(classifieds_price_obj.contract_period)+' Month (s)'
             
            data = {'pay_obj':classified_obj,'level':classifieds_price_obj,'listing_price':sp_cost,'listing_period':duration,'listing_start_date':listing_start_date,'listing_end_date':listing_end_date,'stripe_sp_cost':float(sp_cost*100)}
            data['payment_config']=currency=PaymentConfigure.get_payment_settings()
            if request.method=='POST':
                stripe_token = request.POST.get('stripeToken',False)
                if stripe_token:
                    stripe.api_key = currency.stripe_private_key
                    globalsettings=get_global_settings()
                    try:
                        charge = stripe.Charge.create(
                            amount=int(sp_cost*100), # amount in cents, again
                            currency=currency.currency_code,
                            card=stripe_token,
                            description=request.user.email
                        )
                        po=PaymentOrder(content_object=classified_obj)
                         
                        po.invoice_no=get_invoice_num()
                        po.transactionid=charge.id
                        po.txn_type=''
                        po.payment_mode='Stripe'
                        if charge.paid:
                            po.status='Success'
                            approval_settings=ApprovalSettings.objects.get(name='classifieds')
                            if classified_obj.status=='D':
                                signals.create_staffmail.send(sender=None,object=classified_obj,module='classifieds',action='A',user=request.user)
                            else:
                                signals.create_staffmail.send(sender=None,object=classified_obj,module='classifieds',action='UG',user=request.user)
                            
                            if approval_settings.paid:
                                classified_obj.status='P'
                                try:mail_publish_classifieds(classified_obj)
                                except:pass
                            else:classified_obj.status='N'
                            
                            period=classifieds_price_obj.contract_period
                            
                            classified_obj.payment=classifieds_price_obj
                            classified_obj.listing_start_date=listing_start_date
                            classified_obj.listing_end_date=listing_end_date
                            
                            classified_obj.price=float(sp_cost)
                            if classifieds_price_obj.level=='level2':
                                classified_obj.listing_type='F'
                            elif classifieds_price_obj.level=='level1':
                                classified_obj.listing_type='S'
                            classified_obj.is_paid=True
                            classified_obj.save()  
                            notifictn_type = 'posted as '+classifieds_price_obj.level_label.lower()+' in'
                            signals.create_notification.send(sender=None,user=classified_obj.created_by, obj=classified_obj, not_type=notifictn_type,obj_title=classified_obj.title) 
                        else:po.status='Failed'  
                        po.amount=float(sp_cost)
                        po.start_date = listing_start_date
                        po.end_date =listing_end_date
                        po.user = request.user
                        if classifieds_price_obj:po.listing_type =str(classifieds_price_obj.level_label)+" classifieds"
                        else:po.listing_type =str(classified_obj.get_payment_listing_type())+" classifieds"
                        po.object_name=classified_obj.title
                        po.save()
                        return HttpResponseRedirect(reverse("payments_success", args=["classifieds"]))
                        #return HttpResponseRedirect("/user/payments/?msg=REV&mtype=s")
                    except:
                        data['msg']=PAYMNET_MSG['OOPS']
                        data['mtype']='alert-error'
                else:
                    payment_method = request.POST['payment_options']
                    if 'paypal' in payment_method:
                        form = get_payment_form(
                            item_name=classified_obj.title,
                            price=sp_cost,
                            custom=':'.join(['classifieds',str(classified_obj.id),str(classifieds_price_obj.level),str(request.user.id),str(duration)]),
                            module='classifieds'
                        )
                        data = {'form':form,'module':'classifieds'}
                        return render_to_response("payments/conformation/paypal_submit.html", data, context_instance=RequestContext(request))
                    elif 'authorize' in payment_method:
                        dates = datetime.datetime.now()
                        invoice_id='%s%s%s%s' % (dates.month, dates.day,dates.second,dates.microsecond,)+str(request.user.id)+str(classified_obj.id)
                        payment_settings=PaymentConfigure.get_payment_settings()
                        global_settings=CommonConfigure.objects.only('website_url')[:1][0]
                        params = {
                            'custom': ':'.join(['classifieds',str(classified_obj.id),str(classifieds_price_obj.level),str(request.user.id),str(duration)]),
                            'x_amount': "%.2f" % float(sp_cost),
                            'x_fp_sequence': invoice_id,
                            'x_invoice_num': invoice_id,
                            'x_description': "Items Order Id:"+classified_obj.title ,
                            'x_currency_code':payment_settings.currency_code,
                            'x_fp_timestamp': str(int(time.time())),
                            'x_receipt_link_url': global_settings.website_url+"/user/payments/msg=REV&mtype=i",
                            'x_relay_response':False,
                            }
                        
                        params['x_fp_hash'] = get_fingerprint(invoice_id,params['x_fp_timestamp'],params['x_amount'])
                        forms = SIMPaymentForm(initial=params)
                        
                        if settings.DEBUG:post_url = AUTHNET_TEST_POST_URL
                        else:post_url = AUTHNET_POST_URL
                        
                        data={}
                        data['forms']=forms
                        data['post_url']=post_url
                        data['module']='classifieds'
                        return render_to_response("payments/conformation/authorize_submit.html", data, context_instance=RequestContext(request))

            #################Google Checkout #######################
            else:
                object_id=str(classified_obj.id)
                invoice_id=str(get_invoice_num())
                listing_type=str(classifieds_price_obj.level)
                user_id=str(request.user.id)
                globalsettings=get_global_settings()
                
                c_msg="classifieds:#"+object_id+':#'+invoice_id+':#'+listing_type+':#'+user_id
                fields = {'items': [{'amount':sp_cost,
                                     'name': classified_obj.title,
                                     'description':str(classifieds_price_obj.level_label)+" Classified for "+str(duration),
                                     'id': c_msg,
                                     'currency':currency.currency_code,
                                     'quantity': 1,
                                    }],
                          'return_url': "%s/user/payments/?msg=REV&mtype=s"%(globalsettings.website_url),}
                
                details={'merchant_id':str(currency.merchant_id),'merchant_key':str(currency.merchant_key)}
                google_checkout_obj=GoogleCheckoutIntegration(details)
                google_checkout_obj.add_fields(fields)
                data['gc_obj']= google_checkout_obj
                data['gc_payment_option']=google_checkout_obj.generate_cart_xml
                #################Google Checkout #######################
            
                return render_to_response("payments/conformation/classifieds.html", data, context_instance=RequestContext(request))
        return HttpResponseRedirect(reverse('user_classified_home')+'?msg=OOPS&mtype=e')
    except:
        return HttpResponseRedirect(reverse('user_classified_home')+'?msg=OOPS&mtype=e')

    
@login_required 
def article_payments_confirm(request,aid):
    data={}
    try:
        article = Article.objects.get(id=aid,created_by=request.user)
        pricing = ArticlePrice.objects.filter()[:1][0]
        currency=PaymentConfigure.get_payment_settings()
        if article.article_type == 'FR':
            if pricing.ownstory_is_paid:
                payment = True
                amount = pricing.ownstory_price
            else:payment = False
        elif article.article_type == 'PR':
            if pricing.pressrelease_is_paid:
                payment = True
                amount = pricing.pressrelease_price
            else:payment = False
        elif article.article_type == 'A':
            if pricing.advertorial_is_paid:
                payment = True
                amount = pricing.advertorial_price
            else:payment = False
        else:
            if pricing.requestreview_is_paid:
                payment = True
                amount = pricing.requestreview_price
            else:payment = False
    
        if payment:
            if request.method=='POST':
                stripe_token = request.POST.get('stripeToken',False)
                if stripe_token:
                    stripe.api_key = currency.stripe_private_key
                    globalsettings=get_global_settings()
                    try:
                        charge = stripe.Charge.create(
                            amount=int(amount*100), # amount in cents, again
                            currency=currency.currency_code,
                            card=stripe_token,
                            description=request.user.email
                        )
                        po=PaymentOrder(content_object=article)
                        approval_settings=ApprovalSettings.objects.get(name='article')
                        po.invoice_no=get_invoice_num()
                        po.transactionid=charge.id
                        po.txn_type=''
                        po.payment_mode='Stripe'
                        if charge.paid:
                            po.status='Success'
                            if approval_settings.paid:
                                article.status='P'
                                try:mail_publish_article(article)
                                except:pass
                            else:article.status='N'
                            article.save()
                            signals.create_notification.send(sender=None,user=article.created_by, obj=article, not_type='submitted in',obj_title=article.title)
                            signals.create_staffmail.send(sender=None,object=article,module='articles',action='A',user=request.user)
                            if article.article_type=='FR':article_type_label='Article Own Story'
                            elif article.article_type=='PR':article_type_label='Article Pressrelease'
                            elif article.article_type=='A':article_type_label='Article Advertorial'
                            elif article.article_type=='RR':article_type_label='Article Review Request'
                        else:po.status='Failed'  
                        po.amount=float(amount)
                        po.user = request.user
                        po.listing_type =article_type_label
                        po.object_name=article.title
                        po.save()
                        return HttpResponseRedirect(reverse("payments_success", args=["articles"]))
                    except:
                        data['msg']=PAYMNET_MSG['OOPS']
                        data['mtype']='alert-error'
                else:
                    payment_method = request.POST['payment_options']
                    if 'paypal' in payment_method:
                        form = get_payment_form(article.title,amount,':'.join(['article',str(article.id),str(article.article_type),str(request.user.id)]))
                        data = {'form':form,'module':'article'}
                        return render_to_response("payments/conformation/paypal_submit.html", data, context_instance=RequestContext(request))
                    elif 'authorize' in payment_method:
                        dates = datetime.datetime.now()
                        invoice_id='%s%s%s%s' % (dates.month, dates.day,dates.second,dates.microsecond,)+str(request.user.id)+str(article.id)
                        payment_settings=PaymentConfigure.get_payment_settings()
                        global_settings=CommonConfigure.objects.only('website_url')[:1][0]
                        params = {
                            'custom': ':'.join(['article',str(article.id),str(article.article_type),str(request.user.id)]),
                            'x_amount': "%.2f" % float(amount),
                            'x_fp_sequence': invoice_id,
                            'x_invoice_num': invoice_id,
                            'x_description': "Items Order Id:"+article.title ,
                            'x_currency_code':payment_settings.currency_code,
                            'x_fp_timestamp': str(int(time.time())),
                            'x_receipt_link_url': global_settings.website_url+"/user/payments/msg=REV&mtype=i",
                            'x_relay_response':False,
                            }
                        
                        params['x_fp_hash'] = get_fingerprint(invoice_id,params['x_fp_timestamp'],params['x_amount'])
                        forms = SIMPaymentForm(initial=params)
                        
                        if settings.DEBUG:post_url = AUTHNET_TEST_POST_URL
                        else:post_url = AUTHNET_POST_URL
                        data['forms']=forms
                        data['post_url']=post_url
                        data['module']='classifieds'
                        return render_to_response("payments/conformation/authorize_submit.html", data, context_instance=RequestContext(request))

            data = {'pay_obj':article,'listing_price':amount}
            data['payment_config']=currency
            data['stripe_sp_cost']=float(amount*100)
            #################Google Checkout #######################
            object_id=str(article.id)
            invoice_id=str(get_invoice_num())
            listing_type=str(article.article_type)
            user_id=str(request.user.id)
            
            globalsettings=get_global_settings()
            
            c_msg="article:#"+object_id+':#'+invoice_id+':#'+listing_type+':#'+user_id
            fields = {'items': [{'amount':amount,
                                 'name': article.title,
                                 'description':str(article.get_payment_listing_type()),
                                 'id': c_msg,
                                 'currency':currency.currency_code,
                                 'quantity': 1,
                                }],
                      'return_url': "%s/user/payments/?msg=REV&mtype=s"%(globalsettings.website_url),}
            
            details={'merchant_id':str(currency.merchant_id),'merchant_key':str(currency.merchant_key)}
            google_checkout_obj=GoogleCheckoutIntegration(details)
            google_checkout_obj.add_fields(fields)
            data['gc_obj']= google_checkout_obj
            data['gc_payment_option']=google_checkout_obj.generate_cart_xml
            #################Google Checkout #######################
            data['payment_config']=PaymentConfigure.get_payment_settings()
            return render_to_response("payments/conformation/articles.html", data, context_instance=RequestContext(request))
        else:return HttpResponseRedirect(reverse('article_dash_board')+'?msg=YAS&mtype=s')
    except:return HttpResponseRedirect(reverse('article_dash_board')+'?msg=err&mtype=e')    

@login_required       
def deal_payment(request,did,dpid):
    data ={}
    try:
        deal = Deal.objects.get(id = did)
        dp = DealPayment.objects.get(id = dpid, created_by = request.user)
    except:
        return HttpResponseRedirect(reverse('deal_deals_home')+'?m=error')
    currency=PaymentConfigure.get_payment_settings()
    if request.method=='POST':
        stripe_token = request.POST.get('stripeToken',False)
        if stripe_token:
            stripe.api_key = currency.stripe_private_key
            charge = stripe.Charge.create(
                amount=int(dp.total_price*100), # amount in cents, again
                currency=currency.currency_code,
                card=stripe_token,
                description="DealsPayment - " + request.user.useremail
            )
            po=PaymentOrder(content_object=deal)
            po.invoice_no=get_invoice_num()
            po.transactionid=charge.id
            po.txn_type=''
            po.payment_mode='Stripe'
            if charge.paid:
                po.status='Success'
                deal_payment = dp
                deal_payment.status = 'S'
                    
                deal_payment.transaction_no = charge.id
                deal_payment.is_paid = True
                deal_payment.payment_status = 'Success'
                deal_payment.payer_status = 'Success'
                deal_payment.transaction_type = 'Stripe'
                deal_payment.save()
                signals.create_notification.send(sender=None,user=deal_payment.created_by, obj=deal, not_type='bought as',obj_title=deal.title) 
                signals.create_staffmail.send(sender=None,object=deal,module='deals',action='P',user=request.user)
                try:
                    if deal_payment.is_friend: 
                        buy_success_gift_mail(deal_payment,deal)
                        send_voucher_mail(deal_payment,deal,deal_payment.gift_addr.g_email)
                    else:
                        buy_success_mail(deal_payment,deal)
                        send_voucher_mail(deal_payment,deal,deal_payment.email)
                except:
                    pass
                object_name=deal.get_payment_title()
            else:po.status='Failed' 
            po.amount=float(deal.discount_price)
            po.user = request.user
            po.listing_type ='Purchased Deal(s)'
            po.object_name=object_name
            po.save()
            return HttpResponseRedirect("/payments/deal/success/") #("/user/payments/?msg=REV&mtype=s")
        else:
            payment_method = request.POST['payment_options']
            if 'paypal' in payment_method:
                form = get_deal_payment_form(deal.title,deal.discount_price,dp.quantity,deal.id,':'.join(['deal',str(deal.id),str(dp.id),str(request.user.id)]))
                data = {'form':form,'module':'dashboard'}
                return render_to_response("payments/conformation/paypal_submit.html", data, context_instance=RequestContext(request))
            elif 'authorize' in payment_method:
                dates = datetime.datetime.now()
                invoice_id='%s%s%s%s' % (dates.month, dates.day,dates.second,dates.microsecond,)+str(request.user.id)+str(deal.id)
                payment_settings=PaymentConfigure.get_payment_settings()
                global_settings=CommonConfigure.objects.only('website_url')[:1][0]
                params = {
                    'custom': ':'.join(['deal',str(deal.id),str(dp.id),str(request.user.id)]),
                    'x_amount': "%.2f" % float(deal.discount_price),
                    'x_fp_sequence': invoice_id,
                    'x_invoice_num': invoice_id,
                    'x_description': "Items Order Id:"+deal.title ,
                    'x_currency_code':payment_settings.currency_code,
                    'x_fp_timestamp': str(int(time.time())),
                    'x_receipt_link_url': global_settings.website_url+"/user/payments/msg=REV&mtype=i",
                    'x_relay_response':False,
                    }
                
                params['x_fp_hash'] = get_fingerprint(invoice_id,params['x_fp_timestamp'],params['x_amount'])
                forms = SIMPaymentForm(initial=params)
                
                if settings.DEBUG:post_url = AUTHNET_TEST_POST_URL
                else:post_url = AUTHNET_POST_URL
                
                data={}
                data['forms']=forms
                data['post_url']=post_url
                data['module']='classifieds'
                return render_to_response("payments/conformation/authorize_submit.html", data, context_instance=RequestContext(request))

    data = {'dr': dp}
    data['deal'] = deal
    data['payment_config']=currency
    data['stripe_sp_cost']=float(dp.total_price*100)
    #################Google Checkout #######################
    object_id=str(deal.id)
    invoice_id=str(get_invoice_num())
    listing_type=str(dp.id)
    user_id=str(request.user.id)
    
    globalsettings=get_global_settings()
    
    c_msg="deal:#"+object_id+':#'+invoice_id+':#'+listing_type+':#'+user_id
    fields = {'items': [{'amount':deal.discount_price,
                         'name': deal.title,
                         'description':deal.title,
                         'id': c_msg,
                         'currency':currency.currency_code,
                         'quantity': dp.quantity,
                        }],
              'return_url': "%s/user/payments/?msg=REV&mtype=s"%(globalsettings.website_url),}
    
    details={'merchant_id':str(currency.merchant_id),'merchant_key':str(currency.merchant_key)}
    google_checkout_obj=GoogleCheckoutIntegration(details)
    google_checkout_obj.add_fields(fields)
    data['gc_obj']= google_checkout_obj
    data['gc_payment_option']=google_checkout_obj.generate_cart_xml
    #################Google Checkout #######################
    return render_to_response('payments/conformation/deal.html',data,RequestContext(request)) 
    
    
    
@login_required 
def banner_payments_offline_confirm(request,bid,lid):
    data={}
    #Type = request.GET.get('type')
    banner = BannerAdvertisements.objects.get(id=bid,created_by=request.user)
    payment_object = BannerPayment.objects.get(id=lid)
    
    vv = ContentType.objects.get_for_model(banner)
    total_amounts = banner.temp_amount
    try:
        paid_object = PaymentOrder.objects.filter(content_type=vv,object_id = banner.id).reverse()
        tot = 0
        for bans in paid_object:
            tot = tot+bans.amount
        sp_cost = banner.temp_amount-tot
        
        if sp_cost<1:
            sp_cost=1
    except:
        sp_cost=banner.temp_amount
    
    template = "payments/conformation/banner.html"
    total_amount = sp_cost
    try:
        if request.POST:
            banner.status='N'
            banner.impressions=banner.temp_impressions
            banner.total_amount=banner.temp_amount
            banner.save()
            po=PaymentOrder(content_object=banner)
            po.user = request.user
            po.amount=float(sp_cost)
            po.invoice_no = get_invoice_num()
            po.object_name=banner.caption
            po.status='Pending'
            po.payment_mode='Offline'
            po.phone_no = request.POST.get('pay_phone')
            po.contact_mode = request.POST.get('contact_mode')
            po.email = request.POST.get('pay_email')
            po.offline_mode = request.POST.get('pay_mode')
            po.listing_type =str(payment_object.level)+" Banners"
            po.save()
            messages.success(request, str(BANNER_MSG['BADAS']))
            return HttpResponseRedirect('/user/banners/')
        else:
            data ={'pay_obj':banner,'level':payment_object,'listing_price':total_amount,'payment_object':payment_object,'offline_payment':'offline_payment'}
            return render_to_response(template, data, context_instance=RequestContext(request))
    except:
        messages.error(request, str(BANNER_MSG['OOPS']))
        return HttpResponseRedirect('/user/banners/')
    
@login_required 
def article_payments_offline_confirm(request,aid):
    article = Article.objects.get(id=aid,created_by=request.user)
    pricing = ArticlePrice.objects.filter()[:1][0]
    
    content_type=ContentType.objects.get_for_model(article)
    paid_object = PaymentOrder.objects.filter(content_type__id=content_type.id,object_id = article.id).order_by('-created_on')[0]
    
    data= {}
    try:
        if request.POST:
            article.status='N'
            article.save()
            paid_object.phone_no = request.POST.get('pay_phone')
            paid_object.contact_mode = request.POST.get('contact_mode')
            paid_object.email = request.POST.get('pay_email')
            paid_object.offline_mode = request.POST.get('pay_mode')
            paid_object.save()
            messages.success(request, str(ARTICLE_MSG['YAS']))
            #return HttpResponseRedirect('/user/articles/')
            return HttpResponseRedirect(reverse('payments_success', args=["articles"])+'?type=articles&offline=True')
        else:
            if article.article_type == 'FR' and pricing.ownstory_is_paid:
                    amount = pricing.ownstory_price
            elif article.article_type == 'PR' and pricing.pressrelease_is_paid:
                    amount = pricing.pressrelease_price
            elif article.article_type == 'A' and pricing.advertorial_is_paid:
                    amount = pricing.advertorial_price
            elif pricing.requestreview_is_paid:
                    amount = pricing.requestreview_price
            data= {'pay_obj':article,'paid_object':paid_object,'listing_price':amount}
            return render_to_response("payments/conformation/articles.html", data, context_instance=RequestContext(request))
    except:
        messages.error(request, str(ARTICLE_MSG['OOPS']))
        return HttpResponseRedirect('/user/articles/')

@login_required
def event_payments_offline_confirm(request,eid,lid):
    types = request.REQUEST.get('types','add')
    event = Event.objects.get(id=eid,created_by=request.user)
    event_price_obj = EventPrice.objects.get(id=lid)
    duration = (event.listing_end-event.listing_start)+ timedelta(days=1)
    duration = str(duration).split(',')
    event.listing_duration = duration[0]
    event.save()
    
    content_type=ContentType.objects.get_for_model(event)
    paid_object = PaymentOrder.objects.filter(content_type__id=content_type.id,object_id = event.id).order_by('-created_on')[0]
    amount = event.listing_price
    try:
        if request.POST:
            paid_object.phone_no = request.POST.get('pay_phone')
            paid_object.contact_mode = request.POST.get('contact_mode')
            paid_object.email = request.POST.get('pay_email')
            paid_object.offline_mode = request.POST.get('pay_mode')
            paid_object.save()
            approval_settings = ApprovalSettings.objects.get(name='events')
            event.status = 'N'
            messages.success(request, str(EVENT_MSG['WpMt']))
            if event.payment.level=='level2':
                event.listing_type ='F'
            elif event.payment.level=='level1':
                event.listing_type = 'S'
            event.save()
            #return HttpResponseRedirect('/user/events/')
            return HttpResponseRedirect(reverse('payments_success')+'?type=events&offline=True')
        else:
            data= {'pay_obj':event,'paid_object':paid_object,'event_price':event_price_obj,'listing_price':amount,'listing_start':event.listing_start,'listing_end':event.listing_end,'listing_period':event.listing_duration,'types':types}
            return render_to_response("payments/conformation/events.html", data, context_instance=RequestContext(request))
    except:
        messages.error(request, str(EVENT_MSG['OOPS']))
        return HttpResponseRedirect('/user/events/')
@login_required
def classifieds_payments_offline_confirm(request,cid,lid):
    types = request.REQUEST.get('types','add')
    classified = Classifieds.objects.get(id = cid,created_by=request.user)
    classifieds_price_obj=ClassifiedPrice.objects.get(id = lid)
    
    content_type=ContentType.objects.get_for_model(classified)
    paid_object = PaymentOrder.objects.filter(content_type__id=content_type.id,object_id = classified.id).order_by('-created_on')[0]
    
    period=classifieds_price_obj.contract_period
    listing_start_date=datetime.datetime.now()
    listing_end_date=datetime.date.today()+relativedelta(months=+period)
    duration=str(classifieds_price_obj.contract_period)+' Month (s)'
    #paid_object = PaymentOrder.objects.get(object_id = classified.id)
    approval_settings=ApprovalSettings.objects.get(name='classifieds')
    try:
        if request.POST:
            paid_object.phone_no = request.POST.get('pay_phone')
            paid_object.contact_mode = request.POST.get('contact_mode')
            paid_object.email = request.POST.get('pay_email')
            paid_object.offline_mode = request.POST.get('pay_mode')
            paid_object.save()
            classified.status = 'N'
            classified.save()
            if types == 'update':
                messages.success(request, str(CLASSIFIED_MSG['CUS']))
            else:
                messages.success(request, str(CLASSIFIED_MSG['CAS']))
            #return HttpResponseRedirect('/user/classifieds/')
            return HttpResponseRedirect(reverse('payments_success')+'?type=classifieds&offline=True')
        else:
            data = {'pay_obj':classified,'paid_object':paid_object,'classifieds_price':classifieds_price_obj,'listing_period':duration,'listing_start_date':listing_start_date,'listing_end_date':listing_end_date,'listing_price':classified.price,'types':types}
            return render_to_response("payments/conformation/classifieds.html", data, context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect(reverse('user_classified_home')+'?msg=OOPS&mtype=e')
        
def business_payments_offline_confirm(request,bid,lid):
    business_price_obj=BusinessPrice.objects.get(id=lid)
    try:
        business_obj = Business.objects.get(id=bid,created_by=request.user)
    except:
        # For Business claim created_by user will be a staff. Not the request.user
        business_obj = Business.objects.get(id=bid,created_by__is_staff=True)
    content_type=ContentType.objects.get_for_model(business_obj)
    paid_object = PaymentOrder.objects.filter(content_type__id=content_type.id,object_id = business_obj.id).order_by('-created_on')[0]
    try:
        if request.POST:
            business_obj.status='N'
            business_obj.save()
            paid_object.phone_no = request.POST.get('pay_phone')
            paid_object.contact_mode = request.POST.get('contact_mode')
            paid_object.email = request.POST.get('pay_email')
            paid_object.offline_mode = request.POST.get('pay_mode')
            paid_object.save()
            messages.success(request, str(BUSINESS_MSG['BASTO']))
            return HttpResponseRedirect(reverse('payments_success')+'?type=business&offline=True')
            #return HttpResponseRedirect('/user/business/')
        else:
            try:
                claim=request.REQUEST['c']
                business_obj = Business.objects.get(id=bid)
                if claim!='1' or not business_obj.created_by.is_staff:
                    return HttpResponseRedirect(reverse('user_manage_business')+'?msg=OOPS&mtype=e')
                claim=1
            except:claim=0
                
            payment_type=request.REQUEST['type']
            if payment_type not in ['Y','M']:
                return HttpResponseRedirect(reverse('user_manage_business')+'?msg=OOPS&mtype=e')
            level=business_price_obj.level
            sp_cost=0
            if payment_type=='M':
                if level=='level1':
                    for b_c in business_obj.categories.all():
                        if b_c.price_month:sp_cost=sp_cost+b_c.price_month
                        else:
                            if b_c.parent_cat.price_month:sp_cost=sp_cost+b_c.parent_cat.price_month
                elif level=='level2':
                    sp_cost=business_price_obj.price_month
                   
            elif payment_type=='Y': 
                if level=='level1':
                    for b_c in business_obj.categories.all():
                        if b_c.price_year:sp_cost=sp_cost+b_c.price_year
                        else:
                            if b_c.parent_cat.price_year:sp_cost=sp_cost+b_c.parent_cat.price_year
                elif level=='level2':
                    sp_cost=business_price_obj.price_year
            
            lstart_date=datetime.datetime.now()
            if business_obj.payment_type == 'Y':lend_date=datetime.date.today()+relativedelta(years=+1)
            else:lend_date=datetime.date.today()+relativedelta(months=+1)
            
            data={'claim':claim,'pay_obj':business_obj,'paid_object':paid_object,'business_price':business_price_obj,'level':business_price_obj,'listing_price':sp_cost,'listing_period':payment_type,'lstart_date':lstart_date,'lend_date':lend_date,'stripe_sp_cost':float(sp_cost*100)}
            return render_to_response("payments/conformation/business.html", data, context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect(reverse('user_manage_business')+'?msg=OOPS&mtype=e')

def stripe_list_subscribers(request):
    data ={}
    currency=PaymentConfigure.get_payment_settings()
    stripe.api_key = currency.stripe_private_key
    #globalsettings=get_global_settings()
    try:
        #customers = stripe.Customer.all()
        subscribers = []
        customers = StripePaymentDetails.objects.all()
        for customer in customers:
            subscribers.append(customer)
        data['subscribers'] = subscribers
        return render_to_response("payments/stripe/stripe_list_customers.html", data, context_instance=RequestContext(request))
    except:
        return render_to_response("payments/stripe/stripe_list_customers.html", data, context_instance=RequestContext(request))

def stripe_add_plan(request):
    data ={}
    currency=PaymentConfigure.get_payment_settings()
    stripe.api_key = currency.stripe_private_key
    #globalsettings=get_global_settings()
    if request.POST:
        try:
            Type = request.POST.get("type")
            try:
                oldplan = StripePlanDetails.objects.get(type = Type)
                if oldplan:
                    oldplan.type = 'uncategorized'
                    oldplan.status = "I"
                    oldplan.save()
            except:pass
                
            plan = StripePlanDetails()
            name = request.POST.get("name")
            slug = getUniqueValue(model=StripePlanDetails,proposal = slugify(name), field_name ="plan_id" )
            
            plan.name =request.POST.get("name")
            plan.currency = request.POST.get("currency")
            plan.amount = int(request.POST.get("amount"))
            plan.interval = request.POST.get("interval")
            plan.type = request.POST.get("type")
            plan.status = "A"
            plan.plan_id = slug
            plan.save()
            
            stripeplan = stripe.Plan.create(amount=(plan.amount*100), interval=plan.interval, name=plan.name, currency=plan.currency, id=plan.plan_id)           
            
            return HttpResponseRedirect(reverse('stripe_list_plans')+'?msg=Plan Added Successfully')
        except:
            return HttpResponseRedirect(reverse('stripe_list_plans')+'?msg=Error in adding Plan')
    else:
        return render_to_response("payments/stripe/stripe_add_subscription_plan.html", data, context_instance=RequestContext(request))

def stripe_list_plans(request):
    data ={}
    currency=PaymentConfigure.get_payment_settings()
    stripe.api_key = currency.stripe_private_key
    #globalsettings=get_global_settings()
    data['plans'] = StripePlanDetails.objects.all()
    return render_to_response("payments/stripe/stripe-list-plans.html", data, context_instance=RequestContext(request))

def stripe_plan_details(request, id):
    data={}
    plan = StripePlanDetails.objects.get(id = id)
    data['plan'] = plan
    return render_to_response("payments/stripe/stripe_plan_details.html", data, context_instance=RequestContext(request))
    
def payments_success(request):
    data={}
    type = request.REQUEST.get('type')
    if type == 'photos':
        link = 'photos/purchased/'
    else:
        link = type
    data['type'] = type
    data['link'] = link
    offline = request.REQUEST.get('offline')
    if offline:
        data['offline'] = True
        if type == 'business':data['object'] = 'business'
        elif  type == 'banners':data['object'] = 'banner'
        elif type == 'events':data['object'] = 'event'
        elif type == 'articles':data['object'] = 'article'
        elif type == 'classifieds':data['object'] = 'classified'
        
    return render_to_response("payments/success.html", data, context_instance=RequestContext(request))

def get_stripe_plan_object(interval, amount):
    if amount == 0:
        return None
    try:
        live = stripe.Plan.retrieve("%0.2f-%s-plan" % (amount, interval))
    except:
        live = stripe.Plan.create(
            amount=int(amount*100), 
            interval=interval, 
            name="%0.2f %s plan" % (amount, interval), 
            currency='usd', 
            id="%0.2f-%s-plan" % (amount, interval)
        )
    try:
        plan = StripePlanDetails.objects.get(interval=interval,amount=amount,status='A')
    except:
        plan = StripePlanDetails(
            name="%0.2f %s plan" % (amount, interval),
            plan_id="%0.2f-%s-plan" % (amount, interval),
            currency="usd",
            amount=amount,
            interval =interval,
            type="%s_plan"%(interval),
            status = "A"
        )
        plan.save()
    return plan

def payments_success(request, moduleslug):
    data = {
        "listing_url": {
            "business": reverse("user_manage_business"),
            "events": reverse("events_dash_board"),
            "classifieds": reverse("user_classified_home"),
            "deal": reverse("deal_voucher_list", args=['purchased']),
        }[moduleslug],
        "msgtext": {
            "business": "View and edit your business",
            "events": "View and edit your events",
            "classifieds": "View and edit your classifieds",
            "deal": "View all your purchased deals"
        }[moduleslug],
        "moduleslug": moduleslug,
    }
    return render_to_response("payments/success.html", data, context_instance=RequestContext(request))