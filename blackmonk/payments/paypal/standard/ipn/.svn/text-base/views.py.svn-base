from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from payments.paypal.standard.ipn.forms import PayPalIPNForm
from payments.paypal.standard.ipn.models import PayPalIPN
from payments.paypal.standard.ipn.signals import *


@require_POST
@csrf_exempt
def ipn(request, item_check_callable=None):
    """
    PayPal IPN endpoint (notify_url).
    Used by both PayPal Payments Pro and Payments Standard to confirm transactions.
    http://tinyurl.com/d9vu9d
    
    PayPal IPN Simulator:
    https://developer.paypal.com/cgi-bin/devscr?cmd=_ipn-link-session
    """
    #TODO: Clean up code so that we don't need to set None here and have a lot
    #      of if checks just to determine if flag is set.
    flag = None
    ipn_obj = None
    
    # Clean up the data as PayPal sends some weird values such as "N/A"
    data = request.POST.copy()
    date_fields = ('time_created', 'payment_date', 'next_payment_date',
                   'subscr_date', 'subscr_effective')
    for date_field in date_fields:
        if data.get(date_field) == 'N/A':
            del data[date_field]
    form = PayPalIPNForm(data)
    if form.is_valid():
        try:
            #When commit = False, object is returned without saving to DB.
            ipn_obj = form.save(commit = False)
        except Exception, e:
            flag = "Exception while processing. (%s)" % e
    else:
        flag = "Invalid form. (%s)" % form.errors
    if ipn_obj is None:
        ipn_obj = PayPalIPN()
    
    #Set query params and sender's IP address
    ipn_obj.initialize(request)

    if flag is not None:
        #We save errors in the flag field
        ipn_obj.set_flag(flag)
    else:
        # Secrets should only be used over SSL.
        if request.is_secure() and 'secret' in request.GET:
            ipn_obj.verify_secret(form, request.GET['secret'])
        else:
            ipn_obj.verify(item_check_callable)
    ipn_obj.save()
    return HttpResponse("OKAY")

 
@require_POST
@csrf_exempt
def ipn_old(request, item_check_callable=None):
    context = {}
    flag = None
    ipn_obj = None
    data = request.POST.copy()
    txnid=data.get('txn_id',None)
    if txnid:
        date_fields = ('time_created', 'payment_date', 'next_payment_date','subscr_date', 'subscr_effective')
        try:del data['payment_fee']
        except:pass
        try:del data['ipn_track_id']
        except:pass
        for date_field in date_fields:
            if data.get(date_field) == 'N/A':del data[date_field]
       
        form = PayPalIPNForm(data)
        if form.is_valid():
            try:
                ipn_obj = form.save(commit = False)
                payment_was_successful.send(sender=ipn_obj)################################
            except Exception, e:flag = "Exception while processing. (%s)" % e
        else:flag = "Invalid form. (%s)" % form.errors
        if ipn_obj is None:ipn_obj = PayPalIPN()
        ipn_obj.initialize(request)
        if flag is not None:ipn_obj.set_flag(flag)
        else:
            if request.is_secure() and 'secret' in request.GET:ipn_obj.verify_secret(form, request.GET['secret'])
            else:ipn_obj.verify(item_check_callable)
        ipn_obj.save()
    elif data['txn_type'] in ["subscr_cancel","subscr_eot","subscr_failed","subscr_modify","subscr_payment","subscr_signup"]:
        ipn_objs=PayPalIPN.objects.filter(subscr_id=data['subscr_id'])
        try:ipn_objs.update(**data)
        except:pass
        payment_was_successful.send(sender=ipn_objs[0])################################
    return HttpResponse('OK')
