from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import messages
from common.utils import ds_pagination
from common.models import PaymentConfigure
from payments.models import PaymentOrder
from payments.paypal.standard.ipn.models import PayPalIPN
from business.models import Business
from common.templatetags.ds_utils import get_msg_class_name
from common.staff_messages import PAYMENT_MSG
from payments.stripes.models import StripePaymentDetails,StripePlanDetails, StripeUnsubscribers
import stripe

NO_OF_ITEMS_PER_PAGE=20

######################################################################################################################
###########################################      BUSINESS      #######################################################
######################################################################################################################

@login_required
def view_payment_history(request,template='payments/user/payment_history.html'):
    filter_data = filter(request)
    
    payments=filter_data['payments']
    try:page = int(request.GET['page'])
    except:page=1
    data = ds_pagination(payments,page,'payments',NO_OF_ITEMS_PER_PAGE)
    data['filter']=filter_data['filter']
    data['search']=filter_data['search']
    try:data['msg'] =PAYMENT_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    flag=request.GET.get('tx',None)
    if flag:
        try:
            p_odrer=PaymentOrder.objects.get(transactionid=request.GET['tx'])
            if p_odrer.status=='Success':data['msg'] = PAYMENT_MSG['SUS']
            else:data['msg'] = PAYMENT_MSG['REV']
            data['mtype'] = get_msg_class_name('s')
        except:
            data['msg'] = PAYMENT_MSG['WAI']
            data['mtype'] = get_msg_class_name('i')
    data['sub_list']=["subscr_cancel","subscr_eot","subscr_failed","subscr_modify","subscr_payment","subscr_signup"]
    return render_to_response(template,data, context_instance=RequestContext(request))

@login_required
def ajax_view_payment_history(request,template='payments/user/ajax_payment_history.html'):
    filter_data = filter(request)
    payments=filter_data['payments']
    try:page = int(request.GET['page'])
    except:page=1
    data = ds_pagination(payments,page,'payments',NO_OF_ITEMS_PER_PAGE)
    data['filter']=filter_data['filter']
    data['search']=filter_data['search']
    return render_to_response(template,data, context_instance=RequestContext(request))

def filter(request):
    try:
        try:filter=request.GET['filter']
        except:filter=False
        try:search=request.GET['search']
        except:search=False
        key={}
        key['user']=request.user
        args=()
        if filter:
            if filter=='Paypal' or filter=='Authorize.net' or filter=='Stripe' or filter=='Offline':key['payment_mode']=filter
            elif filter=='Success' or filter=='Pending':key['status']=filter
            else:key['content_type__name']=filter
        if search:
            sub_ids=[p.txn_id for p in PayPalIPN.objects.filter(subscr_id__icontains = search)]
            args=(Q(invoice_no__icontains = search)|Q(transactionid__icontains = search)|Q(transactionid__in = sub_ids)|Q(object_name__icontains = search))
        if key:
            if search:payments = PaymentOrder.objects.filter(args,**key).order_by('-id')
            else:payments = PaymentOrder.objects.filter(**key).order_by('-id')
        else:
            if search:payments = PaymentOrder.objects.filter(args).order_by('-id')
            else:payments = PaymentOrder.objects.filter(**key).order_by('-id')
    except:
        payments = PaymentOrder.objects.filter(**key).order_by('-id')
    return {'payments':payments,'search':search,'filter':filter}

@login_required
def ajax_payment_details(request,id,template='payments/user/transaction_details.html'):
    data = {}
    payment = PaymentOrder.objects.get(id = id)
    if payment.payment_mode == 'Stripe':
        try:
            stripe_object = StripePaymentDetails.objects.get(subscription_id=payment.transactionid)
            data['stripe_object']=stripe_object
        except:pass
    data['payment']=payment
    return render_to_response(template,data, context_instance=RequestContext(request))
    
from common.mail_utils import business_unsubscribe_staff_notification
from payments.stripes.models import StripePaymentDetails,StripeUnsubscribers
@login_required
def business_unsubscribe(request,id):
    try:
        stripe_object = StripePaymentDetails.objects.get(object_id=id ,subscription_status='active')
    except:
        stripe_object = None
    if request.POST:
        stripe_unsub = StripeUnsubscribers()
        stripe_unsub.stripe_details = stripe_object
        stripe_unsub.email = request.POST.get('emailid')
        stripe_unsub.mobile = request.POST.get('phoneno')
        stripe_unsub.reason = request.POST.get('reason')
        stripe_unsub.save()
        stripe_object.subscription_status = 'onhold'
        stripe_object.save()
        business_unsubscribe_staff_notification(stripe_object.id)
        return HttpResponse('1')
    else:
        data = {'stripe_object':stripe_object}
        return render_to_response('payments/user/stripe_unsubscribe.html',data, context_instance=RequestContext(request))
    
    
@login_required
def update_stripe_card_detail(request, id):
    data = {}
    spd = StripePaymentDetails.objects.get(id=id)
    currency=PaymentConfigure.get_payment_settings()
    stripe.api_key = currency.stripe_private_key
    customer = stripe.Customer.retrieve(spd.customer_id) 
    if request.method == "POST":
        card = request.POST.get('stripeToken')
        if card is not None:
            customer.card = card
            customer.email = request.POST.get('stripeEmail')
            customer.save()
            messages.success(request, "Your card has been updated successfully.")
    data['spd'] = spd
    data['payment_config'] = currency
    data['customer'] = customer
    return render_to_response('payments/user/stripe_card_update.html', data, context_instance=RequestContext(request))