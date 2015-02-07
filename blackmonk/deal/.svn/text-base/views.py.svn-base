from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.paginator import Paginator
from django.template import RequestContext
from django.db.models import Sum
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.translation import gettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.conf import settings as my_settings
from django.utils import simplejson
from django.db.models import Count

from deal.models import Deal,DealCategory,DealPayment,Faqs,How,Subscribe
from deal.forms import GiftedAddressForm,ContactForm,RedeemForm,DealAddressForm, UserDealAddressForm
from deal.utils import get_rem_seconds,get_seconds,set_numberof_views,get_todays_deals,send_mail_contact,get_voucher_key
from common.utils import ds_pagination, get_global_settings
from locality.models import Locality
#from usermgmt.models import Profile
from django.utils import simplejson

from django.template import  Template,Context
from usermgmt.adminviews import  *
from payments.utils import *
from common.models import ModuleNames

import datetime
from datetime import timedelta
from time import strptime

messages = {'suc': _("Thank you for Purchasing , Your order number is %s, <br/>Your discount Voucher will be send to your email."),
            'fsuc': _("Thank you for Purchasing, Your order number is %s,<br/> Your discount Voucher will be send to your friend's email."),
            'limit': _("'Sorry! You are entitled to buy only %d coupons.'"),
            'clos': _("Sorry! This deal is closed. Check out more deals at <a href='/deals/'>Today's Deal</a>"),
            'nnn': _("Thank you for Purchasing deal, <br/>Your order details will be send to your email."),
            'error':_("Not able to process your request! Please try later"),
            'unsub':_("You have Unsubscribed Successfully")
            }

ITEMS_PER_PAGE = 9

def reset_deal_quantity():
    #Reset Quantity 
    try:
        now = datetime.datetime.now()
        d_qnty_chk = DealPayment.objects.filter(is_paid = False,status__in='[P,E]')
        for chk in d_qnty_chk:
            dts = chk.created_on + timedelta(minutes=10)
            if now > dts:
                chk.quantity = 0
                chk.save()
    except:pass            
    #Reset Quantity    

def deals_home(request, catslug='all', template='default/deals/deals-home.html'):
    fetched_values = ['title','slug','about','original_price','discount_price','end_date']
    ''' updating deals availability '''
    reset_deal_quantity() 
    today = datetime.date.today()
    try:category = DealCategory.objects.get(slug = catslug)
    except:category = False
    categories = DealCategory.objects.all()
    featured_deals =  Deal.objects.only(*fetched_values).filter(status='P',featured = True, end_date__gte=today, start_date__lte=today).order_by('?')[:4]
    
    if not category:
        deals = Deal.objects.only(*fetched_values).filter(end_date__gte=today, start_date__lte=today, status='P').order_by('-created_on')
        url = reverse('deal_deals_home')
    else:
        deals = Deal.objects.only(*fetched_values).filter(end_date__gte=today, start_date__lte=today, status='P', category = category).order_by('-created_on')
        url =  reverse('deals_category_listing',args = [category.slug]) 
    
    page = int(request.GET.get('page',1))      
    data = ds_pagination(deals,page,'deals',ITEMS_PER_PAGE)
    if 'm' in request.REQUEST:
        message = request.GET.get('m',False)
        data['message']= message
    data['featured_deals'] = featured_deals        
    data['seo'] = ModuleNames.get_module_seo(name='deals')
    data['url'] = url
    data['category'] = category
    data['categories'] = categories
    data['view_type'] = request.GET.get('view','grid')
    try:
        message = messages[request.GET['m']]
        data['message'] = message
    except:pass
    return render_to_response(template ,data, RequestContext(request))

def deal_details(request, slug='all', template='default/deals/deal-details.html'):
    data = {}
    today = datetime.date.today()
    try:
        deal = Deal.objects.select_related('category').get(slug=slug,status='P')
    except:
        return HttpResponseRedirect(reverse('deal_deals_home'))
    set_numberof_views(deal,request)
    if 'm' in request.REQUEST:
        message = request.GET.get('m',False)
        data['message']= message
    data['deal']= deal
    rem_seconds = get_rem_seconds(deal,today)
    if rem_seconds <= 0:
        data['rem_seconds']= False
    else:
        data['rem_seconds']= rem_seconds
    return render_to_response(template ,data, RequestContext(request))


def ajax_nearestdeal_search(request):
    try:
        name=request.GET['q']
        locality = Locality.objects.filter(name__icontains=name).order_by('name')[:10]
    except:
        locality = Locality.objects.all().order_by('name')[:10]
    results = []
    for l in locality:
        results.append(l.name)
    return HttpResponse('\n'.join(results), mimetype='text/plain')


@login_required
def confirmation(request, template='default/deals/confirmation.html'):
    reset_deal_quantity()
    data = {}
    today = datetime.date.today()
    try: data['faqs'] = Faqs.objects.all().order_by('id')
    except:data['faqs'] = False
    data['seo'] = ModuleNames.get_module_seo(name='deals')
    try:
        deal = Deal.objects.get(id=request.REQUEST['did'],status='P',end_date__gte=today)
        data['deal'] = deal
    except:
        return HttpResponseRedirect(reverse('deal_deals_home')+'?m='+str(messages['error']))
    try:
        data['friend'] = request.REQUEST['friend']
        friend = True
    except:friend = False
    if request.method == 'GET':
        DealPayment.objects.filter(created_by=request.user, is_paid=False, deal=deal).delete()
    deal_limit_chk = DealPayment.objects.filter(created_by=request.user, deal=deal).aggregate(limited_cnt=Sum('quantity'))
    if deal_limit_chk['limited_cnt']:
        data['user_limited_cnt'] = deal_lmt_chk =  deal_limit_chk['limited_cnt']
    else:
        data['user_limited_cnt'] = deal_lmt_chk = 0
    if deal.limit_per_customer <= deal_limit_chk['limited_cnt'] and deal.limit_per_customer !=0:
        return HttpResponseRedirect(reverse('deals_deal_details',args=[deal.slug, '.html'])+'?id=%d&m=%s'%(deal.id,eval(messages['limit']+"%("+str(deal.limit_per_customer)+")")))
    deal_total_chk = DealPayment.objects.filter(deal=deal).aggregate(total_cnt=Sum('quantity'))
    if deal_total_chk['total_cnt']:deal_toal_chk =  deal_total_chk['total_cnt']
    else:deal_toal_chk = 0
    if deal.max_count <= deal_total_chk['total_cnt']:
        return HttpResponseRedirect(reverse('deal_deals_home')+'?id=%d&m=%s'%(deal.id,messages['clos']))
    
    if request.method == 'POST':
        quantity = request.POST.get('quantity','1')
        try:
            gdt_addr_obj = GiftedAddress.objects.get(id=request.POST['gfr_addr_id'])
            formf = GiftedAddressForm(request.POST,instance=gdt_addr_obj)
        except:
            formf = GiftedAddressForm(request.POST)
        if friend:
            if formf.is_valid():
                formf.save()
            else:
                data['formf'] = formf
                data['form'] = UserDealAddressForm(request.POST)
                return render_to_response(template, data, RequestContext(request))
        form = UserDealAddressForm(request.POST)
        if form.is_valid():
            addess_form = form.save(commit=False)

            if deal.limit_per_customer < int(deal_lmt_chk)+int(quantity) and deal.limit_per_customer !=0:
                return HttpResponseRedirect(reverse('deal_deals_home')+'?id=%d&m=%s'%(deal.id,eval(messages['limit']+"%("+str(deal.limit_per_customer)+")")))
            if deal.max_count < int(deal_toal_chk)+int(quantity):
                return HttpResponseRedirect(reverse('deal_deals_home')+'?id=%d&m=%s'%(deal.id,messages['clos']))
            
            addess_form.created_by = request.user
            addess_form.deal = deal
            addess_form.quantity = quantity
            addess_form.quantity_static = quantity
            addess_form.unit_price = deal.discount_price
            addess_form.total_price = int(quantity) * int(deal.discount_price)
            addess_form.dealkey = get_voucher_key(deal)
            if friend:
                addess_form.is_friend = True
                addess_form.gift_addr = formf.instance
            addess_form.save()
        else:
            data['form'] = form
            data['gif_addr'] = formf.instance
            data['formf'] = GiftedAddressForm(request.POST,instance=formf.instance)
            return render_to_response(template, data, RequestContext(request))
        if addess_form:
            return HttpResponseRedirect(reverse('deal_payment',args=[deal.id,addess_form.id]))
        else:
            return HttpResponseRedirect(reverse('deal_deals_home')+'?m='+str(messages['error']))
    else:
        form_data={
           'name':request.user.display_name,
           'address':request.user,
           'mobile':request.user.mobile,
           'email':request.user.useremail,
        }
        form=UserDealAddressForm(initial=form_data)
        data['form']=form
        data['count_limits'] = range(1, min(deal.max_count - deal.get_total_reg_count(), deal.limit_per_customer - deal_lmt_chk) + 1)
        if friend :data['formf'] = GiftedAddressForm()
        return render_to_response(template, data, RequestContext(request))  
      

#################  Manage Merchant Reedem ################
@login_required
def redeem(request):
    data ={}
    if request.method == 'POST':
        form = RedeemForm(request.POST)
        if form.is_valid():
            deal_pymnt = DealPayment.objects.get(dealkey = form.cleaned_data.get('voucher_key'))
            data['deal_pymnt'] = deal_pymnt
            return render_to_response('default/deals/redeem_dealinformation.html',data,RequestContext(request))
        else:
            data['form']=form
    else:
        try:message = request.GET['m']
        except:message = False  
        data['message'] = message  
        data['form'] = RedeemForm()
    return render_to_response('default/deals/redeem.html',data,RequestContext(request))    

@login_required
def confirm_redeem(request):
    today=datetime.datetime.now()
    if request.method == 'POST':
       try:
           deal_pymnt = DealPayment.objects.get(id = request.GET['dr'])
           if deal_pymnt.status == 'S':
               if deal_pymnt.deal.voucher_valid >= today.date():
                   deal_pymnt.status = 'D'
                   deal_pymnt.delivered_date = datetime.datetime.now()
                   deal_pymnt.save()
                   message= _("Successfully redeemed !")
               else:
                   message= _("Sorry ,This voucher is out of date !")
           else:
               message= _("This voucher already redeemed or blocked !")
       except:
           message= _("You can't redeem this voucher !")
    else:
        message= _("You have no permission to access this page !")
    return HttpResponseRedirect(reverse('deal_redeem')+'?m=%s'%(message))

###################### 

def ajax_subscribe(request):
    data={}
    try:mail = request.POST['email']
    except:mail=False
    if mail:
        try:objt = Subscribe.objects.get(email = mail)
        except:objt = False
        if objt:
            data['msg'] = "You already subscribed !."
        else:
            try:
                user = User.objects.get(email = mail)
                obj = Subscribe(created_by = user,email = user.email)
                obj.save()
                data['msg'] = "Thanks! Will update you with new deals"
            except:
                obj = Subscribe(email = mail)
                obj.save()
                data['msg'] = "Thanks! Will update you with new deals."
    else:
        data['msg'] = "Sorry! Not able to process your request."
    
    return HttpResponse(simplejson.dumps(data))
      
@login_required
def invite(request):
    data = {}
    #invitation = JoinInvitation(from_user=request.user,to_mail=to_email,confirmation_key=profile.invitation_key)
    #invitation.save()
    return render_to_response('default/deals/invite.html',data,RequestContext(request))
        
def ajax_tell_a_friend(request):
    global_settings = get_global_settings()
    scaptcha={}
    if request.method == 'POST':
        deal = Deal.objects.get(id=request.POST['content_id'])
        from_name = request.POST['from_name']
        to_name = request.POST['to_name']
        #subject = request.POST['subject']
        msg = request.POST['msg']
        ################# Send MAil #####################  
        to_emailid = request.POST['to_email']
        
        subject = global_settings.domain+' - '+from_name+' send you the "'+deal.title+'" deal details'
        tell_a_friend_data={ "from_name": from_name,
                    "to_name": to_name,"message": msg,"deal": deal,"link":deal.get_email_absolute_url()}
        email_message = render_to_string("default/deals/mail_tell_a_friend.html",tell_a_friend_data,context_instance=RequestContext(request))
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,[to_emailid])
        email.content_subtype = "html"
        ################# Send MAil #####################            
        email.send()
#        try:
#            profile = Profile.objects.get(pk=request.user.id)
#            try:
#                User.objects.get(email=to_email)
#            except:
#                invitation = JoinInvitation(from_user=request.user,to_mail=to_email,confirmation_key=profile.invitation_key)
#                invitation.save()
#        except:pass
        scaptcha['success'] = 1
        data  = simplejson.dumps(scaptcha)
        return HttpResponse(data)
    else:
        scaptcha['success'] = 0
        data  = simplejson.dumps(scaptcha)
        return HttpResponse(data)


def how(request):
    data = {}
    try:data['seo'] = ModuleNames.get_module_seo(name='deals')
    except:data['seo'] = False
    try:data['how_description'] = How.objects.get(heading = 'dcr')
    except:data['how_description'] = False
    try:data['how'] = How.objects.all().exclude(heading = 'dcr').order_by('id')
    except:data['how'] = False
    return render_to_response('default/deals/how.html',data,RequestContext(request))

def faqs(request):
    data = {}
    try: data['faqs'] = Faqs.objects.all().order_by('id')
    except:data['faqs'] = False
    try:data['seo'] = ModuleNames.get_module_seo(name='deals')
    except:data['seo'] = False
    return render_to_response('default/deals/businessfaqs.html',data,RequestContext(request))
    

def contact(request, template='default/deals/contact-us.html'):
    data = {}
    if request.method != 'POST':
        data['form']= ContactForm()
    else:
        form =  ContactForm(request.POST)
        if form.is_valid():
            send_mail_contact(request,form.cleaned_data.get('name'),form.cleaned_data.get('mobile'), form.cleaned_data.get('email'), form.cleaned_data.get('details'))
            data['form'] = ContactForm()
            data['message'] = _("Thanks for contacting us, we'll get back to you shortly.")
        else:
            data['form'] = form
    try:data['seo'] = ModuleNames.get_module_seo(name='deals')
    except:data['seo'] = False       
    return render_to_response(template, data, RequestContext(request))

################## Account  ####################
@login_required
def order_details(request):
    data = {}
    try:page = int(request.GET['page'])
    except:page = 1
    deal_payment = DealPayment.objects.filter(created_by=request.user,status__in='[D,S,E]')
    data = ds_pagination(deal_payment,page,'deal_payment',5)
    data['base_url'] = '/deals/dashboard/'
    data['deals'] = Deal.objects.filter(deal_by__email=request.user.email)
    
    deals_state = DealPayment.objects.values('status').filter(created_by = request.user,status__in='[S,D]').annotate(s_count=Count('status'))
    total = 0
    STATE={'S':0,'D':0}
    for st in deals_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    data['purchased'] =STATE['D']
    data['pending'] =STATE['S']
    data['total'] = total
    return render_to_response('deal/user/order-details.html', data, RequestContext(request))

@login_required
def ajax_payment_detail(request):
    data={}
    try:
        payment = DealPayment.objects.get(id=request.GET['pid'])
        data['payment']=payment
        return render_to_response('default/deals/user_payment_detail.html',data,context_instance=RequestContext(request))
    except:
        return HttpResponse(_('Oops!..error while retrieving payment detail, data not found'))

def deal_unsubscribe(request,id):
    try:
        deal=Subscribe.objects.get(id=id)
        if request.method=='POST':
            deal.delete()
            return HttpResponseRedirect(reverse('deal_deals_home')+'?m='+str(messages['unsub']))
        else:
            data={'id':id}
            return render_to_response('default/deals/unsubscribe.html',data,context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect(reverse('deal_deals_home')+'?msg=OOPS')