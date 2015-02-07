from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.paginator import Paginator
from django.template import RequestContext
from django.db.models import Sum
from django.db.models import Count
from django.contrib.auth import get_user_model
from common.utils import ds_pagination, get_global_settings
from deal.models import Deal,DealCategory,DealPayment,Faqs,How,Subscribe
import datetime

@login_required
def order_list(request, orders='purchased'):
    data = {}
    try:page = int(request.GET['page'])
    except:page = 1
    if orders == 'vouchers':
        deal_payment = DealPayment.objects.filter(deal__merchant=request.user).order_by('-created_on')
    elif orders == 'purchased':
        deal_payment = DealPayment.objects.filter(created_by=request.user,status__in='[D,S,E]').order_by('-created_on')
    data = ds_pagination(deal_payment,page,'deal_payment',5)
    data['base_url'] = '/deals/dashboard/'
    data['deals'] = Deal.objects.filter(deal_by__email=request.user.email)
    
    deals_state = deal_payment.values('status').annotate(s_count=Count('status'))
    total = 0
    STATE={'S':0,'D':0,'P':0}
    for st in deals_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    data['purchased'] =STATE['D']
    data['pending'] =STATE['S']
    data['total'] = total
    data['active'] = orders
    return render_to_response('deal/user/order-details.html', data, RequestContext(request))

@login_required
def user_deal_order_details(request,id):
    data = {}
    deal_payment = DealPayment.objects.get(id=id)
    data['deal_payment'] = deal_payment
    return render_to_response('deal/user/user_order_details.html', data, RequestContext(request))

@login_required
def redeem_voucher(request):
    if request.method == "POST":
        voucher = DealPayment.objects.get(id=request.POST['voucher'])
        voucher.delivered_date = datetime.datetime.now()
        voucher.status = request.POST['status']
        voucher.save()
        return HttpResponse('0')
    return HttpResponse('1')
