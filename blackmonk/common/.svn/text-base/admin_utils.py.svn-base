from django.utils import simplejson
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth import get_user_model
from common.templatetags.ds_utils import get_msg_class_name
from common.models import StaffEmailSettings,AvailableApps
User = get_user_model()

def get_emailsettings(name):
    try:
        emailsettings=StaffEmailSettings.objects.filter(availableapps__name__iexact=name)
        data={}
        for es in emailsettings:
            data["a_"+es.action]=True
            data["e_"+es.action]=es.emails
        return data
    except:pass

def save_emailsettings(request,name):
    try:
        on_add=request.POST.get('on_add',False)
        on_update=request.POST.get('on_update',False)
        on_claim=request.POST.get('on_claim',False)
        on_purchase=request.POST.get('on_purchase',False)
        save_emailsetting(name,'A',request.POST.get('on_update_email',request.user.email),on_add)
        save_emailsetting(name,'U',request.POST.get('on_update_email',request.user.email),on_update)
        save_emailsetting(name,'C',request.POST.get('on_claim_email',request.user.email),on_claim)
        save_emailsetting(name,'P',request.POST.get('on_purchase_email',request.user.email),on_purchase)
    except:
        pass
    
def save_emailsetting(name,action,email,save):
    try:
        emailsettings=StaffEmailSettings.objects.get(availableapps__name__iexact=name,action=action)
        if not save:emailsettings.delete()
    except:
        if save:emailsettings=StaffEmailSettings(availableapps=AvailableApps.objects.get(name__iexact=name),action=action)
    if save:
        emailsettings.emails=email
        emailsettings.save()
    return True

def success_response_to_save_category(append_data,data,template,MSG):
    """
    HTML TO APPEND IN LISTING PAGE AND DISPLAY IN LIGHTBOX AFTER ADDING/UPDATING AN CATEGORY
    """
    try:
        if data['cat']:
            msg = str(MSG['CUS'])
        else:
            msg = str(MSG['CAS'])
    except:
        msg = str(MSG['CUS'])
    lightbox_html=render_to_string(template,data)
    append_html=render_to_string('admin/portal/common/append_category_list.html',append_data)
    send_data={'append_html':append_html, 'lightbox_html':lightbox_html,'status':True,'msg':msg,'mtype':get_msg_class_name('s'),'id':append_data['cat'].id}
    return HttpResponse(simplejson.dumps(send_data))

def success_response_to_save_parent_category(append_data,data,template,MSG,parent):
    """
        HTML TO APPEND IN LISTING PAGE AND DISPLAY IN LIGHTBOX AFTER AJAX ADDING/UPDATING AN CATEGORY/Parent Category
    """
    lightbox_html=render_to_string(template,data)
    if not parent:
        append_html=render_to_string('admin/portal/common/append_parent_category_list.html',append_data)
    else:
        append_html=render_to_string('admin/portal/common/append_sub_category_list.html',append_data)
    if parent:parent=1
    else:parent=0
    send_data={'append_html':append_html,'parent':parent,'lightbox_html':lightbox_html,'status':1,'msg':str(MSG['CUS']),'mtype':get_msg_class_name('s'),'id':append_data['cat'].id,'success':True}
    if parent:
        try:send_data['parent_id']=append_data['cat'].parent.id
        except:send_data['parent_id']=append_data['cat'].parent_cat.id
    else:send_data['parent_id']=None
    return HttpResponse(simplejson.dumps(send_data))


def error_response(data,template,MSG):
    """
    HTML TO DISPLAY IN LIGHTBOX IN CASE OF ERROR WHILE ADDING/UPDATING AN CATEGORY/PARENT-CATEGORY/ATTRIBUTE/FORUM/LOCALITY
    """
    lightbox_html=render_to_string(template,data)
    send_data={'lightbox_html':lightbox_html,'status':False,'msg':str(MSG['OOPS']),'mtype':get_msg_class_name('e')}
    return HttpResponse(simplejson.dumps(send_data))
   
def response_delete_category(request,model,MSG):
    """
    DELETE CATEGORY COMMON METHOD FOR CATEGORY
    """
    try:
        try:
            id=[cid.strip() for cid in request.GET['id'].split(',') if cid.strip()]
        except:
            id=request.GET['id']
        cat = model.objects.filter(id__in=id)
        cat.delete()
        status=1
        msg=MSG['CDS']
        mtype='s'
    except:
        status=0
        msg=MSG['OOPS']
        mtype='e'
    data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return data

def success_response_to_save_forum(append_data,data,template,MSG):
    """
    HTML TO APPEND IN LISTING PAGE AND DISPLAY IN LIGHTBOX AFTER ADDING/UPDATING AN FORUM-TOPIC
    """
    lightbox_html=render_to_string(template,data)
    append_html=render_to_string('admin/portal/common/append_forum_list.html',append_data)
    send_data={'append_html':append_html, 'lightbox_html':lightbox_html,'status':True,'msg':str(MSG['TUS']),'mtype':get_msg_class_name('s'),'id':append_data['cat'].id}
    return HttpResponse(simplejson.dumps(send_data))

def response_delete_forum(request,model,MSG):
    """
       AFTER FORUM TOPIC DELETE
    """
    try:
        try:id=request.GET['id'].split(',')
        except:id=request.GET['id']
        cat = model.objects.filter(id__in=id)
        cat.delete()
        status=1
        msg=MSG['TDS']
        mtype='s'
    except:
        status=0
        msg=MSG['OOPS']
        mtype='e'
    data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return data

def response_to_save_settings(request,status,data,template,MSG):
    """
       RENDER HTML AFTER AJAX SAVE SETTINGS
    """
    html=render_to_string(template,data,context_instance=RequestContext(request))
    if status:
        msg=str(MSG['SUS'])
        mtype=get_msg_class_name('s')
    else:
        msg=str(str(MSG['OOPS']))
        mtype=get_msg_class_name('e')
    send_data={'html':html,'status':status,'msg':msg,'mtype':mtype}
    return HttpResponse(simplejson.dumps(send_data))

def response_to_save_attribute(request,append_data,data,template,MSG,bus=None,group=None):
    """
    HTML TO APPEND IN LISTING PAGE AND DISPLAY IN LIGHTBOX AFTER ADDING/UPDATING AN ATTRIBUTE/GROUP
    """
    if data['attributes'] != None:
        msg = 'AUS'
    else:
        msg = 'AAS'
    lightbox_html=render_to_string(template,data,context_instance=RequestContext(request))
    if group:
        append_html=render_to_string('admin/portal/common/append_attribute_group_list.html',append_data)
    else:
        append_html=render_to_string('admin/portal/common/append_attribute_list.html',append_data)
    send_data={'append_html':append_html,'lightbox_html':lightbox_html,'status':1,'msg':str(MSG[msg]),'mtype':get_msg_class_name('s'),'id':append_data['cat'].id}
    if not group:
        if bus:send_data['parent']=append_data['cat'].attribute.id
        else:send_data['parent']=append_data['cat'].category.id
    return HttpResponse(simplejson.dumps(send_data))

def response_to_save_paymentoption(request,append_data,data,template,MSG,):
    if data['attribute'] != None:
        msg = 'POUS'
    else:
        msg = 'POAS'
    lightbox_html=render_to_string(template,data,context_instance=RequestContext(request))
    append_html=render_to_string('admin/portal/common/append_attribute_group_list.html',append_data)
    send_data={'append_html':append_html,'lightbox_html':lightbox_html,'status':1,'msg':str(MSG[msg]),'mtype':get_msg_class_name('s'),'id':append_data['cat'].id}
    return HttpResponse(simplejson.dumps(send_data))

def response_delete_paymentoption(request,model,MSG):
    """
    AJAX DELETE ATTRIBUTE
    """
    try:
        try:id=request.GET['id'].split(',')
        except:id=request.GET['id']
        cat = model.objects.filter(id__in=id)
        cat.delete()
        status=1
        msg=MSG['PODS']
        mtype='s'
    except:
        status=0
        msg=MSG['OOPS']
        mtype='e'
    data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return data

def response_delete_attribute(request,model,MSG):
    """
    AJAX DELETE ATTRIBUTE
    """
    try:
        try:id=request.GET['id'].split(',')
        except:id=request.GET['id']
        cat = model.objects.filter(id__in=id)
        cat.delete()
        status=1
        msg=MSG['ADS']
        mtype='s'
    except:
        status=0
        msg=MSG['OOPS']
        mtype='e'
    data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return data

def response_delete_attribute_bus(request,model,MSG,group):
    """
    AJAX DELETE ATTRIBUTE-GROUP-BUSINESS 
    """
    try:
        try:id=request.GET['id']
        except:id=None
        try:id=id.split(',')
        except:id=id
        attribute = model.objects.filter(id__in=id)
        attribute.delete()
        if group:msg=str(MSG['GDS'])
        else:msg=str(MSG['ADS'])
        status=1
        mtype='s'
    except:
        status=0
        msg=str(MSG['OOPS'])
        mtype='e'
    data={'status':status,'msg':msg,'mtype':get_msg_class_name(mtype)}
    return data

def success_response_to_save_locality(append_data,data,template,MSG,type=None):
    """
    HTML TO APPEND IN LISTING PAGE AND DISPLAY IN LIGHTBOX AFTER AJAX ADDING/UPDATING AN ZIPCODE/VENUE
    """
    lightbox_html=render_to_string(template,data)
    append_html=render_to_string('admin/portal/common/append_location_list.html',append_data)
    if type:msg=str(MSG['TUS'])
    else:msg=str(MSG['ZUS'])
    send_data={'append_html':append_html, 'lightbox_html':lightbox_html,'status':1,'msg':msg,'mtype':get_msg_class_name('s'),'id':append_data['cat'].id}
    return HttpResponse(simplejson.dumps(send_data))

def response_delete_locality(request,model,MSG,type='Z'):
    """
    AJAX DELETE ZIPCODE/VENUE COMMON METHOD
    """
    try:
        try:id=request.GET['id'].split(',')
        except:id=request.GET['id']
        cat = model.objects.filter(id__in=id)
        cat.delete()
        status=1
        if type=='V':msg=MSG['VDS']
        elif type=='T':msg=MSG['TDS']
        else:msg=MSG['ZDS']
        mtype='s'
    except:
        status=0
        msg=MSG['OOPS']
        mtype='e'
    data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return data

def success_response_to_save_genre_lang(append_data,data,template,MSG,type='G'):
    """
    HTML TO APPEND IN LISTING PAGE AND DISPLAY IN LIGHTBOX AFTER ADDING/UPDATING AN MOVIES-GENRE/LANGUAGE
    """
    lightbox_html=render_to_string(template,data)
    if type=='L':append_data['type']=True
    else:append_data['type']=False
    if type=='C':append_html=render_to_string('admin/portal/common/append_criticsource_list.html',append_data)
    else:append_html=render_to_string('admin/portal/common/append_genre_lang_list.html',append_data)
    send_data={'append_html':append_html, 'lightbox_html':lightbox_html,'status':True,'mtype':get_msg_class_name('s'),'id':append_data['cat'].id}
    if type=='L': 
        try:
            if data['cat']:
                msgl = str(MSG['LUS'])
            else:
                msgl = str(MSG['LAS'])
        except:
            msgl = str(MSG['LUS'])
        send_data['msg']=msgl
        
    elif type=='C':
        try:
            if data['cat']:
                msgc = str(MSG['CUS'])
            else:
                msgc = str(MSG['CAS'])
        except:
            msgc = str(MSG['CUS']) 
        send_data['msg']=msgc
        
    else:
        try:
            if data['cat']:
                msg = str(MSG['GUS'])
            else:
                msg = str(MSG['GAS'])
        except:
            msg = str(MSG['GUS'])
        send_data['msg']=msg
    return HttpResponse(simplejson.dumps(send_data))

def response_delete_genre_lang(request,model,MSG,type='L'):
    """
    AJAX DELETE MOVIES-GENRE/LANGUAGE COMMON METHOD
    """
    try:
        try:id=request.GET['id'].split(',')
        except:id=request.GET['id']
        cat = model.objects.filter(id__in=id)
        cat.delete()
        status=1
        if type=='L':msg=MSG['LDS']
        elif type=='C':msg=MSG['CDS']
        else:msg=MSG['GDS']
        mtype='s'
    except:
        status=0
        msg=MSG['OOPS']
        mtype='e'
    data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return data

def success_response_create_user(append_data,append_template,data,template,MSG,request):
    """
    HTML TO APPEND IN LISTING PAGE AND DISPLAY IN LIGHTBOX AFTER ADDING/UPDATING A USER ACCOUNT
    """
    lightbox_html=render_to_string(template,data,context_instance=RequestContext(request))
    append_html=render_to_string(append_template,append_data,context_instance=RequestContext(request))     
    send_data={'append_html':append_html, 'lightbox_html':lightbox_html,'status':True,'msg':str(MSG),'mtype':get_msg_class_name('s'),'id':append_data['profile'].id}
    return HttpResponse(simplejson.dumps(send_data))

def error_response_create_user(data,template,MSG,request):
    """
    HTML TO DISPLAY IN LIGHTBOX IN CASE OF ERROR WHILE ADDING/UPDATING A USER ACCOUNT
    """
    lightbox_html=render_to_string(template,data,context_instance=RequestContext(request))
    send_data={'lightbox_html':lightbox_html,'status':False,'msg':str(MSG),'mtype':get_msg_class_name('e')}     
    return HttpResponse(simplejson.dumps(send_data))
   
def get_unique_username(username):
    from random import choice,randint
    while True:
        try:
            user = User.objects.get(display_name = username)
            uinque_id = ''.join([choice('123456789') for i in range(3)])
            username+=uinque_id
        except:
            return username        

def success_response_to_save_provider(append_data,data,template,MSG):
    """
    HTML TO APPEND IN LISTING PAGE AND DISPLAY IN LIGHTBOX AFTER ADDING/UPDATING AN CATEGORY
    """
    lightbox_html=render_to_string(template,data)
    append_html=render_to_string('admin/portal/common/append_provider_list.html',append_data)
    send_data={'append_html':append_html, 'lightbox_html':lightbox_html,'status':True,'msg':str(MSG['PUS']),'mtype':get_msg_class_name('s'),'id':append_data['cat'].id}
    return HttpResponse(simplejson.dumps(send_data))


def response_delete_provider(request,model,MSG):
    """
    DELETE CATEGORY COMMON METHOD FOR CATEGORY
    """
    try:
        try:id=request.GET['id'].split(',')
        except:id=request.GET['id']
        cat = model.objects.filter(id__in=id)
        cat.delete()
        status=1
        msg=MSG['PDS']
        mtype='s'
    except:
        status=0
        msg=MSG['OOPS']
        mtype='e'
    data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return data   

def success_response_to_save_qanda(append_data,data,template,MSG):
    """
    HTML TO APPEND IN LISTING PAGE AND DISPLAY IN LIGHTBOX AFTER ADDING/UPDATING AN QANDA
    """
    lightbox_html=render_to_string(template,data)
    append_html=render_to_string('admin/portal/common/append_qanda_list.html',append_data)
    send_data={'append_html':append_html,'lightbox_html':lightbox_html,'status':True,'msg':str(MSG['QAUS']),'mtype':get_msg_class_name('s'),'id':append_data['qanda'].id}
    return HttpResponse(simplejson.dumps(send_data))

def response_delete_qanda(request,model,MSG):
    """
    DELETE QANDA METHOD FOR SWEEPSTAKES
    """
    try:
        try:id=request.GET['id'].split(',')
        except:id=request.GET['id']
        cat = model.objects.filter(id__in=id)
        cat.delete()
        status=1
        msg=MSG['QADS']
        mtype='s'
    except:
        status=0
        msg=MSG['OOPS']
        mtype='e'
    data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return data
