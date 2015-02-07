import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.contenttypes.models import ContentType
import json
from random import choice, randint

from common.models import CommonConfigure, PaymentConfigure
from payments.models import PaymentOrder, OfflinePayment
from payments.paypal.standard.forms import PayPalPaymentsForm


def get_invoice_num():
    while True:
        tid = ''.join([choice('ABCDEFGHKLNPRSTUWX345679') for i in range(8)])
        try:
            PaymentOrder.objects.only('id').get(invoice_no=tid)
        except:
            return tid
def get_payment_form(item_name,price,custom,module=None):
    payment_settings=PaymentConfigure.get_payment_settings()
    cconf = CommonConfigure.objects.only('website_url')[:1][0]
    paypal_dict = {
        "cmd": "_xclick",
        "business": payment_settings.paypal_receiver_email,
        "amount": price,
        "item_name": item_name,
        "custom": custom,
        "invoice": get_invoice_num(),
        "item_number": randint(10000,99999),
        "mc_currency": payment_settings.currency_code,
        "mc_currency":payment_settings.currency_code,
        "notify_url": "%s/payments/paypal/notify/"%(cconf.website_url),
        "return_url": "%s/user/payments/" % (cconf.website_url) if module is None else "%s/payments/%s/success/" % (cconf.website_url, module),
        "cancel_return": "%s/user/payments/?msg=CAN&mtype=s" % (cconf.website_url),
        }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return form 
   
def get_recurring_payment_form(item_name,price,subscription_type,custom):
    payment_settings=PaymentConfigure.get_payment_settings()
    cconf = CommonConfigure.objects.only('website_url')[:1][0]
    paypal_dict = {
        "cmd": "_xclick-subscriptions",
        "business": payment_settings.paypal_receiver_email,
        "a3":price,                        # monthly price 
        "p3": 1,        # duration of each unit (depends on unit)
        "t3": subscription_type,           # duration unit ("M for Month")
        "src": "1",                        # make payments recur
        "sra": "1",                        # reattempt payment on payment error
        "no_note": "1",                    # remove extra notes (optional)
        "item_name": item_name ,
        "custom":custom,
        "currency_code": payment_settings.currency_code, 
        "mc_currency":payment_settings.currency_code,
        "notify_url": "%s/payments/paypal/notify/" % (cconf.website_url),
        "return_url": "%s/payments/business/success/" % (cconf.website_url),
        "cancel_return": "%s/user/business" % (cconf.website_url),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return form    
   
def get_deal_payment_form(item_name,price,quantity,deal_id,custom):
    payment_settings=PaymentConfigure.get_payment_settings()
    cconf = CommonConfigure.objects.only('website_url')[:1][0]
    paypal_dict = {
        "cmd": "_xclick",
        "business": payment_settings.paypal_receiver_email,
        "amount": price,
        "item_name": item_name,
        "quantity": quantity,
        "custom":custom,
        "invoice": get_invoice_num(),
        "item_number":deal_id,
        "currency_code": payment_settings.currency_code, 
        "mc_currency":payment_settings.currency_code,
        "notify_url": "%s/payments/paypal/notify/"%(cconf.website_url),
        "return_url": "%s/user/payments/"%(cconf.website_url),
        "cancel_return": "%s/user/payments/?msg=CAN&mtype=s"%(cconf.website_url),
        }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return form 

def get_shop_paypal_form(item_name,price,custom):
    payment_settings=PaymentConfigure.get_payment_settings()
    cconf = CommonConfigure.objects.only('website_url')[:1][0]
    paypal_dict = {
        "cmd": "_xclick",
        "business": payment_settings.paypal_receiver_email,
        "amount": price,
        "item_name": item_name,
        "custom":custom,
        "invoice": get_invoice_num(),
        "item_number":randint(10000,99999),
        "currency_code": payment_settings.currency_code, 
        "mc_currency":payment_settings.currency_code,
        "notify_url": "%s/payments/paypal/notify/"%(cconf.website_url),
        "return": "%s/user/payments/"%(cconf.website_url),
        "cancel_return": "%s/user/shop/orders/"%(cconf.website_url),
        }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return form 

def save_to_offline_payment(**kwargs):
    next_month = datetime.datetime.now() + relativedelta(months=+1)
    obj = kwargs.pop('object')
    try:
        ctype = ContentType.objects.get_for_model(obj)
        payobj = OfflinePayment.objects.get(
            content_type=ctype,
            object_id=obj.id,
            status='N'
        )
    except:
        payment_status = kwargs.get('status', 'N')
        if payment_status != 'N':
            return True
        else:
            payobj = OfflinePayment(
                content_object=obj,
                expiry_date=kwargs.get('expiry_date', next_month),
            )
    if kwargs.get('amount') is not None:
        payobj.amount = kwargs.pop('amount')
    if kwargs.get('status') is not None:
        payobj.status = kwargs.pop('status')

    if payobj.moredetails: moredetails = json.loads(payobj.moredetails)
    else: moredetails = dict()
    for key in kwargs: moredetails[key] = kwargs[key]
    payobj.moredetails = json.dumps(moredetails)
    payobj.save()

    return True