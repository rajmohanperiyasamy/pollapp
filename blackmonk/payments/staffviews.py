from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Q

from common.utils import ds_pagination
from payments.models import PaymentOrder
from payments.paypal.standard.ipn.models import PayPalIPN

NO_OF_ITEMS_PER_PAGE=20

######################################################################################################################
###########################################      BUSINESS      #######################################################
######################################################################################################################


@staff_member_required
#@permission_required('business.publish_business',raise_exception=True)
def view_payment_history(request,template='payments/staff/payment_history.html'):
    """
    try:
        po=PaymentOrder.objects.all()
        for p in po:
            if p.content_object:
                p.object_name=p.content_object.get_payment_title()
            else:
                p.object_name=str(p.content_type.name)
            p.save()
    except:pass
    """
    filter_data = filter(request)
    payments=filter_data['payments']
    try:page = int(request.GET['page'])
    except:page=1
    data = ds_pagination(payments,page,'payments',NO_OF_ITEMS_PER_PAGE)
    data['filter']=filter_data['filter']
    data['search']=filter_data['search']
    data['sub_list']=["subscr_cancel","subscr_eot","subscr_failed","subscr_modify","subscr_payment","subscr_signup"]
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
#@permission_required('business.publish_business',raise_exception=True)
def ajax_view_payment_history(request,template='payments/staff/ajax_payment_history.html'):
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
        args=()
        if filter:
            if filter=='Paypal' or filter=='Googlecheckout' or filter=='Offline' or filter=='Stripe':key['payment_mode']=filter
            elif filter=='Success' or filter=='Pending':key['status']=filter
            else:key['content_type__name']=filter
        if search:
            sub_ids=[p.txn_id for p in PayPalIPN.objects.filter(subscr_id__icontains = search)]
            args=(Q(invoice_no__icontains = search)|Q(transactionid__icontains = search)|Q(transactionid__in = sub_ids))
        
        if key:
            if search:payments = PaymentOrder.objects.filter(args,**key).order_by('-id')
            else:payments = PaymentOrder.objects.filter(**key).order_by('-id')
        else:
            if search:payments = PaymentOrder.objects.filter(args).order_by('-id')
            else:payments = PaymentOrder.objects.all().order_by('-id')
    except:payments = PaymentOrder.objects.all().order_by('-id')
    return {'payments':payments,'search':search,'filter':filter}

def ajax_offline_payment(request,id,template='payments/staff/ajax_offline_payment.html'):
    data = {}
    id = id
    payment  = PaymentOrder.objects.get(id = id)
    if request.POST:
        payment.email = request.POST.get('emailid')
        payment.phone_no = request.POST.get('phone')
        payment.offline_mode = request.POST.get('payment_mode') 
        ch_dd_no = request.POST.get('cheque_dd_num')
        if ch_dd_no:
            payment.cheque_dd_num = ch_dd_no
        payment.status = 'Success'
        payment.save()
        return HttpResponseRedirect(reverse('staff_view_payment_history'))
    else:
        data['payment'] = payment
        return render_to_response(template,data, context_instance=RequestContext(request))