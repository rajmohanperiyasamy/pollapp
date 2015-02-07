from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect  
from django.core.urlresolvers import reverse
from django.utils import simplejson


from common.admin_utils import error_response,success_response_to_save_category
from common.templatetags.ds_utils import get_msg_class_name
from usermgmt.decorators import admin_required
from bmshop.products.models import Category,DeliveryTime,Manufacturer
from bmshop.products.forms import CategoryForm,DeliveryTimeForm,ManufactureForm
from bmshop.static_msgs import ADMIN_MSG

from django.contrib.auth import get_user_model
User = get_user_model()
@admin_required
def category_settings(request,template='admin/portal/bmshop/category.html'):
    category_objs = Category.objects.all().order_by('name')
    data = {'category_objs':category_objs}
    try:data['msg'] =ADMIN_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def category_update(request,template='admin/portal/bmshop/update_category.html'):
    data={}
    category=None
    try:
        category = Category.objects.get(id = request.REQUEST['id'])
        form=CategoryForm(instance=category)
    except:
        form=CategoryForm()
    
    if request.method == "POST":
        
        if category:form=CategoryForm(request.POST,instance=category)
        else: form=CategoryForm(request.POST)
        
        if form.is_valid():
            form.save()
            send_data={'status':1}
        else:
            lightbox_html=render_to_string(
                        template,{'form':form,'cat':category},
                        context_instance=RequestContext(request)
                        )
            send_data={'lightbox_html':lightbox_html,'status':0}
        return HttpResponse(simplejson.dumps(send_data))
    else:
        data = {'form':form,'cat':category}
        return render_to_response(template,data,context_instance=RequestContext(request))

@admin_required
def delete_category(request):
    try:
        cat = Category.objects.filter(id=request.GET['id'])
        cat.delete()
        status=1
        msg=ADMIN_MSG['CDD']
        mtype='s'
    except:
        status=0
        msg=ADMIN_MSG['OOPS']
        mtype='e'
    data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return HttpResponse(simplejson.dumps(data))    

@admin_required
def delivery_time(request,template='admin/portal/bmshop/deliverytime.html'):
    dtime_obj = DeliveryTime.objects.all().order_by('-id')
    data = {'dtime_obj':dtime_obj}
    
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def update_delivery_time(request,template='admin/portal/bmshop/include_dlvrytime.html'):
    data={}
    d_time=None
    try:
        d_time = DeliveryTime.objects.get(id = request.REQUEST['id'])
        form=DeliveryTimeForm(instance=d_time)
        flag = True
    except:
        form=DeliveryTimeForm()
        flag = False
    
    if request.method == "POST":
        if d_time:form=DeliveryTimeForm(request.POST,instance=d_time)
        else: form=DeliveryTimeForm(request.POST)
        if form.is_valid():
            d_time = form.save()
            
            lightbox_html=render_to_string(template,{'form':form,'d_time':d_time})
            
            append_html=render_to_string('admin/portal/bmshop/append_dlvy_time.html',{'d_time':d_time})
            
            if flag:
                send_data={'append_html':append_html,
                            'lightbox_html':lightbox_html,
                            'status':1,'msg':str(ADMIN_MSG['DUS']),
                            'mtype':get_msg_class_name('s'),'id':d_time.id}
            else:
                send_data={'append_html':append_html,
                            'lightbox_html':lightbox_html,
                            'status':1,'msg':str(ADMIN_MSG['DAS']),
                            'mtype':get_msg_class_name('s'),'id':d_time.id}
                
            return HttpResponse(simplejson.dumps(send_data))
        
        else:
            lightbox_html=render_to_string(template,{'form':form,'d_time':d_time})
            
            send_data={'lightbox_html':lightbox_html,'status':0}
            
            return HttpResponse(simplejson.dumps(send_data))
    else:
        data = {'form':form,'d_time':d_time}
        return render_to_response(template,data,context_instance=RequestContext(request))
    
@admin_required
def delete_delivery_time(request):
    try:
        try:id=request.GET['id'].split(',')
        except:id=request.GET['id']
        cat = DeliveryTime.objects.filter(id__in=id)
        cat.delete()
        status=1
        msg=ADMIN_MSG['DTS']
        mtype='s'
    except:
        status=0
        msg=ADMIN_MSG['OOPS']
        mtype='e'
    data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return HttpResponse(simplejson.dumps(data))    
    
@admin_required
def manufactures(request,template='admin/portal/bmshop/manufactures.html'):
    mn_objs = Manufacturer.objects.all().order_by('name')
    data = {'mn_objs':mn_objs}
    return render_to_response (template, data, context_instance=RequestContext(request))   

@admin_required
def update_manufactures(request,template='admin/portal/bmshop/update_manufactures.html'):
    data={}
    mn_obj=None
    try:
        mn_obj = Manufacturer.objects.get(id = request.REQUEST['id'])
        form=ManufactureForm(instance=mn_obj)
    except:form=ManufactureForm()
    
    if request.method == "POST":
        
        if mn_obj:form=ManufactureForm(request.POST,instance=mn_obj)
        else: form=ManufactureForm(request.POST)
        
        if form.is_valid():
            mn_obj = form.save()
            lightbox_html=render_to_string(
                    template,
                    {'form':form,'mn_obj':mn_obj},
                    context_instance=RequestContext(request))
            
            append_html=render_to_string('admin/portal/bmshop/append_manufacture.html',{'mn_obj':mn_obj})
        
            send_data={'append_html':append_html,
                        'lightbox_html':lightbox_html,
                        'status':1,'msg':str(ADMIN_MSG['PUD']),
                        'mtype':get_msg_class_name('s'),'id':mn_obj.id}
            return HttpResponse(simplejson.dumps(send_data))
        
        else:
            lightbox_html=render_to_string(
                        template,{'form':form,'mn_obj':mn_obj},
                        context_instance=RequestContext(request))
            send_data={'lightbox_html':lightbox_html,'status':0}
            return HttpResponse(simplejson.dumps(send_data))
    else:
        data = {'form':form,'mn_obj':mn_obj}
        return render_to_response(template,data,context_instance=RequestContext(request))
   

@admin_required
def delete_manufactures(request):
    try:
        try:id=request.GET['id'].split(',')
        except:id=request.GET['id']
        cat = Manufacturer.objects.filter(id__in=id)
        cat.delete()
        status=1
        msg=ADMIN_MSG['MDS']
        mtype='s'
    except:
        status=0
        msg=ADMIN_MSG['OOPS']
        mtype='e'
    data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return HttpResponse(simplejson.dumps(data))      
