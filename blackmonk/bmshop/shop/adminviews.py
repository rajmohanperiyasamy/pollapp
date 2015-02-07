
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect  
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.db.models import Count
from django.conf import settings
from django.contrib import messages

from common.admin_utils import error_response,success_response_to_save_category
from common.templatetags.ds_utils import get_msg_class_name
from common.models import PaymentConfigure
from usermgmt.decorators import admin_required
from bmshop.shop.models import Shop,PymentSettings,Shipping
from bmshop.shop.forms import ShopSettingsForm,PaymentSettingsForm,ShippingForm
from bmshop.products.models import Category,Product
from bmshop.static_msgs import ADMIN_MSG


User = settings.AUTH_USER_MODEL
@admin_required
def admin_settings(request,template='admin/portal/bmshop/settings.html'):
    featured=0
    approval=None
    total=0
    STATE={'P':0,'B':0}
    category=Category.objects.all().count()

    product_state = Product.objects.values('featured','is_active','status').annotate(s_count=Count('status'),f_count=Count('featured'))

    for st in product_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
       if st['featured']:
            featured+=st['f_count']

    data={
          'published':STATE['P'],
          'blocked':STATE['B'],
          'featured':featured,
          'category':category,
          'total':total,
    }
    shop_obj = Shop.get_shop_settings()
    if shop_obj:form = ShopSettingsForm(instance=shop_obj)
    else:form = ShopSettingsForm()
    data['form']=form
    try:data['msg'] =ADMIN_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def update_admin_settings(request,template='admin/portal/bmshop/settings.html'):
    shop_obj = Shop.get_shop_settings()
    if shop_obj:form = ShopSettingsForm(instance=shop_obj)
    else:form = ShopSettingsForm()
    if request.method == 'POST':
        if shop_obj:form = ShopSettingsForm(request.POST,instance=shop_obj)
        else:form = ShopSettingsForm(request.POST)
        if form.is_valid():
            shop=form.save(commit=False)
            shop.created_by=request.user
            shop.save()
            form.save_m2m()
            messages.success(request, str(ADMIN_MSG['SUS']))
            return HttpResponseRedirect(reverse('admin_bmshop_main_settings'))
    data = {'form':form}
    return render_to_response (template, data, context_instance=RequestContext(request))        

def payment_settings(request,template='admin/portal/bmshop/include_paymentsetting.html'):
    pay_obj = PymentSettings.get_pay_settings()
    if pay_obj:form = PaymentSettingsForm(instance=pay_obj)
    else:form = PaymentSettingsForm()
    payment_config=PaymentConfigure.get_payment_settings()
    
    if request.method=='POST':
        if pay_obj:form = PaymentSettingsForm(request.POST,instance=pay_obj)
        else:form = PaymentSettingsForm(request.POST) 
        if form.is_valid():
            form.save()
            args={'form':form,'payment_config':payment_config}
            html=render_to_string(template,args, context_instance=RequestContext(request))
            data={'html':html,'status':1,'msg':str(ADMIN_MSG['PUS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(data)) 
        else:
            args={'form':form,'payment_config':payment_config}
            html=render_to_string(template,args, context_instance=RequestContext(request))
            data={'html':html,'status':0}
            return HttpResponse(simplejson.dumps(data)) 
    data = {'form':form,'payment_config':payment_config}
    return render_to_response ('admin/portal/bmshop/payment_settings.html', data, context_instance=RequestContext(request))

def shipping_settings(request,template='admin/portal/bmshop/include_shipping_settings.html'):
    ship_obj = Shipping.get_shippment_settings()
    if ship_obj:
        form = ShippingForm(instance=ship_obj)
    else:
        form = ShippingForm()

    if request.method == 'POST':
        if ship_obj:
            form = ShippingForm(request.POST,instance=ship_obj)
        else:
            form = ShippingForm(request.POST) 
        if form.is_valid():
            ship_obj = form.save(commit=False)
            ship_obj.active = True
            ship_obj.save()
            html=render_to_string(template,{'form':form}, context_instance=RequestContext(request))
            data={'html':html,'status':1,'msg':str(ADMIN_MSG['SSU']),'mtype':get_msg_class_name('s')}
        else:
            html=render_to_string(template,{'form':form}, context_instance=RequestContext(request))
            data={'html':html,'status':0}
        return HttpResponse(simplejson.dumps(data))
    
    data = {'form':form}
    return render_to_response ('admin/portal/bmshop/shipping.html', data, context_instance=RequestContext(request))    


def auto_suggest_email(request):
    try:data = User.objects.filter(email__icontains=request.GET['term'])[:10]
    except:data = User.objects.all()[:10]
    response_dict = {}
    child_dict = []
    response_dict.update({'results':child_dict})
    mytags=[]
    for obj in data :
        b={'label':obj.email,'id':obj.id,'value':obj.email}
        mytags.append(b)
    return HttpResponse(simplejson.dumps(mytags))
