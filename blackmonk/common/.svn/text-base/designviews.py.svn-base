#Python Libs

#Django Libs and Methods
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils import simplejson

#Application Libs and Common Methods
from common.templatetags.ds_utils import get_msg_class_name
from common.static_msg import DESIGN_MSG
from common.getunique import getUniqueValue
from usermgmt.decorators import admin_required

#Module Files(models,forms etc...)
from common.designforms import UpdateMenuForm
from common.models import AvailableModules, CommonConfigure  
from django.core.cache import cache 

"""
#####################################################################################################################
############################### ADMIN DESIGN CONFIGURATION ##########################################################
#####################################################################################################################
"""

@admin_required
def design_overview(request):
    ''' displays design config page '''
    return HttpResponseRedirect(reverse('admin_design_manage_navigation'))#admin_design_manage_navigation

@admin_required
def manage_navigation(request, template='admin/design/manage-content-navigation.html'):
    ''' method for managing header,sub header menu content'''
    data={}
    data['main_menus'] = AvailableModules.objects.filter(level='header',parent__isnull=True,is_active=True).order_by('order')
    data['disabled_main_menus']= AvailableModules.objects.filter(level='header',parent__isnull=True,is_active=False).order_by('order')
    cache.clear()
    return render_to_response (template, data, context_instance=RequestContext(request))


@admin_required    
def update_menu_positions(request):
    ''' method for updating order of header menu items '''
    sortlist = request.GET['sortlist'].split(',')
    try:
        for position,item in enumerate(sortlist):
            m_item = item.split('=')
            sub_menu_id = m_item[1]
            main_menu_id=m_item[0].split('[')[1].split(']')[0]
            if sub_menu_id == 'root':
                try:
                    sub_menu_obj = AvailableModules.objects.get(id=int(main_menu_id),level='submenu')
                    sub_menu_obj.parent=None
                    sub_menu_obj.level = 'header'
                    sub_menu_obj.save()
                except:pass    
                try:
                    menu_obj = AvailableModules.objects.get(id=int(main_menu_id),level='header')
                    menu_obj.order = position
                    menu_obj.save()
                except:pass    
            else:
                smenuid=m_item[0].split('[')[1].split(']')[0]
                try:
                    main_menu_obj = AvailableModules.objects.get(id=int(smenuid))
                    main_menu_obj.parent_id=int(sub_menu_id)
                    main_menu_obj.level = 'submenu'
                    main_menu_obj.save()
                except:pass 
                try:
                    sub_menu_obj = AvailableModules.objects.get(id=int(smenuid),parent__id=int(sub_menu_id),level='submenu')
                    sub_menu_obj.order = position
                    sub_menu_obj.save()
                except:pass 
    except:
        pass
    return_data = {'msg':str(DESIGN_MSG['HMOS']),'mtype':get_msg_class_name('s')}
    cache.clear()
    return HttpResponse(simplejson.dumps(return_data))
    
    
@admin_required    
def reset_menu_positions(request,template='admin/design/include-header-navigation.html'):
    ''' method for resetting order of header menu items '''
    data={}
    data['main_menus'] = AvailableModules.objects.filter(level='header',parent__isnull=True).order_by('order')
    
    html=render_to_string(template,data,context_instance=RequestContext(request))
    return_data = {'html':html}
    cache.clear()
    return HttpResponse(simplejson.dumps(return_data))
    
    
@admin_required    
def update_menu_item(request,template='admin/design/update-menu-item.html'):    
    ''' method for add/update header menu item '''
    data={}
    try:
        menu_obj = AvailableModules.objects.get(id=request.REQUEST['mid'])
        edit=True
    except:
        menu_obj = False
        edit=False
            
    if not request.POST:
        if menu_obj:form = UpdateMenuForm(instance=menu_obj)
        else:form = UpdateMenuForm()
    else:
        if menu_obj:form = UpdateMenuForm(request.POST,instance=menu_obj)
        else:form = UpdateMenuForm(request.POST)
        if form.is_valid():
            menu_update_form = form.save(commit=False)
            menu_update_form.slug = getUniqueValue(AvailableModules,slugify(menu_update_form.base_url),instance_pk=menu_update_form.id)
            menu_update_form.level = 'header'
            menu_update_form.save()
                    
            mdata={'new_menu_obj':menu_update_form}
            menu_list_html = render_to_string('admin/design/append-menu-content.html',mdata,context_instance=RequestContext(request))
            
            data = {'form':form,'menu_obj':menu_obj}
            html=render_to_string(template,data,context_instance=RequestContext(request))
            return_data = {'html':html, 'menu_list_html':menu_list_html,'status':True,'edit':edit,'id':menu_update_form.id,'msg':str(DESIGN_MSG['MIAS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(return_data))
        else:
            data = {'form':form,'menu_obj':menu_obj}
            html=render_to_string(template,data,context_instance=RequestContext(request))
            return_data = {'html':html,'status':False,'msg':str(DESIGN_MSG['OOPS'])}
            return HttpResponse(simplejson.dumps(return_data))
    data = {'form':form,'menu_obj':menu_obj}    
    cache.clear()    
    return render_to_response (template, data, context_instance=RequestContext(request)) 
    
    
@admin_required
def delete_menu_item(request):
    ''' method for deleting header,sub header menu item '''
    try:
        menu_obj = AvailableModules.objects.get(id=request.GET['mid'])
        menu_obj.delete()
        return_data = {'success':True,'msg':str(DESIGN_MSG['MIDS']),'mtype':get_msg_class_name('s')}
    except:
        return_data = {'success':False,'msg':str(DESIGN_MSG['OOPS']),'mtype':get_msg_class_name('e')}
    cache.clear()
    return HttpResponse(simplejson.dumps(return_data))
    
        
@admin_required        
def manage_subheader_navigation(request, template='admin/design/manage-subheader-navigation.html'):
    ''' method for managing sub header menu contents '''
    data={}
    data['sub_header_menus'] = AvailableModules.objects.filter(level='exp',parent__isnull=True,is_active=True).order_by('order')
    data['disabled_sub_header_menus'] = AvailableModules.objects.filter(level='exp',parent__isnull=True,is_active=False).order_by('order')
    cache.clear()
    return render_to_response (template, data, context_instance=RequestContext(request))

        
@admin_required            
def update_subheader_item(request,template='admin/design/update-subheader-item.html'):    
    ''' method for add/update sub header menu item '''
    data={}
    try:
        menu_obj = AvailableModules.objects.get(id=request.REQUEST['mid'],level='exp')
        edit=True
    except:
        menu_obj = False
        edit=False
            
    if not request.POST:
        if menu_obj:form = UpdateMenuForm(instance=menu_obj)
        else:form = UpdateMenuForm()
    else:
        if menu_obj:form = UpdateMenuForm(request.POST,instance=menu_obj)
        else:form = UpdateMenuForm(request.POST)
        if form.is_valid():
            menu_update_form = form.save(commit=False)
            menu_update_form.slug = getUniqueValue(AvailableModules,slugify(menu_update_form.base_url),instance_pk=menu_update_form.id)
            menu_update_form.level = 'exp'
            menu_update_form.save()
            mdata={'new_menu_obj':menu_update_form}
            menu_list_html = render_to_string('admin/design/append-subheader-content.html',mdata,context_instance=RequestContext(request))
            
            data = {'form':form,'menu_obj':menu_obj}
            html=render_to_string(template,data,context_instance=RequestContext(request))
            return_data = {'html':html, 'menu_list_html':menu_list_html,'status':True,'edit':edit,'id':menu_update_form.id,'msg':str(DESIGN_MSG['SMIAS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(return_data))
        else:
            data = {'form':form,'menu_obj':menu_obj}
            html=render_to_string(template,data,context_instance=RequestContext(request))
            return_data = {'html':html,'status':False,'msg':str(DESIGN_MSG['OOPS'])}
            return HttpResponse(simplejson.dumps(return_data))
            
    data = {'form':form,'menu_obj':menu_obj}        
    cache.clear()
    return render_to_response (template, data, context_instance=RequestContext(request))        
    

@admin_required    
def update_subheader_positions(request):
    ''' method for updating orders of sub header menu items '''
    #list[60]=root,list[58]=60,list[54]=root,list[55]=root,list[56]=root,list[57]=root,list[53]=root,list[59]=root,list[71]=root,list[73]=root
    data = request.GET['sortlist'].split(',')
    return_data = {}
    try:
        for position,menu_item in enumerate(data):
            menu, parent = menu_item.split('=')
            menu_obj = AvailableModules.objects.get(id=int(menu[5:-1]))
            if parent == 'root':
                menu_obj.parent = None
                menu_obj.level = 'exp'
            else:
                menu_obj.parent = AvailableModules.objects.get(id=int(parent))
                menu_obj.level = 'sub-exp'
            menu_obj.order = position
            menu_obj.save()
        return_data = {'msg':str(DESIGN_MSG['SHMOS']),'mtype':get_msg_class_name('s')}
    except:
        return_data = {'msg':str(DESIGN_MSG['OOPS']),'mtype':get_msg_class_name('e')}
    cache.clear()
    return HttpResponse(simplejson.dumps(return_data))


@admin_required    
def manage_copyright(request,template='admin/design/manage-copyright.html'):
    ''' method for managing copyright informations '''
    try:copyright_obj = CommonConfigure.objects.all()[:1][0]
    except:copyright_obj=False
    data={'copyright_obj':copyright_obj}  
    cache.clear()
    return render_to_response (template, data, context_instance=RequestContext(request))  
    
    
@admin_required      
def update_copyright_info(request,template='admin/design/include-copyright-settings.html'):
    ''' method for updating copyright information '''
    copyright_obj = CommonConfigure.objects.all()[:1][0]
    copyright_obj.copyright = request.POST['copyright']
    copyright_obj.save()
    
    data={'copyright_obj':copyright_obj}  
    html=render_to_string(template,data,context_instance=RequestContext(request))
    return_data = {'html':html,'msg':str(DESIGN_MSG['CIUS']),'mtype':get_msg_class_name('s')}
    cache.clear()
    return HttpResponse(simplejson.dumps(return_data))  

@admin_required
def manage_footer(request, template='admin/design/manage-content-footer.html'):
    ''' method for managing footer menu content'''
    data={}
    data['footer_menus'] = AvailableModules.objects.filter(level='footer',parent__isnull=True,is_active=True).order_by('order')
    data['disabled_footer_menus']= AvailableModules.objects.filter(level='footer',parent__isnull=True,is_active=False).order_by('order')
    cache.clear()
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required    
def update_footer_item(request,template='admin/design/update-footer-item.html'):    
    ''' method for add/update footer menu item '''
    data={}
    try:
        menu_obj = AvailableModules.objects.get(id=request.REQUEST['mid'])
        edit=True
    except:
        menu_obj = False
        edit=False
            
    if not request.POST:
        if menu_obj:form = UpdateMenuForm(instance=menu_obj)
        else:form = UpdateMenuForm()
    else:
        if menu_obj:form = UpdateMenuForm(request.POST,instance=menu_obj)
        else:form = UpdateMenuForm(request.POST)
        if form.is_valid():
            menu_update_form = form.save(commit=False)
            menu_update_form.slug = getUniqueValue(AvailableModules,slugify(menu_update_form.base_url),instance_pk=menu_update_form.id)
            if not menu_obj:
                menu_update_form.level = 'footer'
            menu_update_form.save()
                    
            mdata={'new_menu_obj':menu_update_form}
            menu_list_html = render_to_string('admin/design/append-footer-content.html',mdata,context_instance=RequestContext(request))
            
            data = {'form':form,'menu_obj':menu_obj}
            html=render_to_string(template,data,context_instance=RequestContext(request))
            return_data = {'html':html, 'menu_list_html':menu_list_html,'status':True,'edit':edit,'id':menu_update_form.id,'msg':str(DESIGN_MSG['FIAS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(return_data))
        else:
            data = {'form':form,'menu_obj':menu_obj}
            html=render_to_string(template,data,context_instance=RequestContext(request))
            return_data = {'html':html,'status':False,'msg':str(DESIGN_MSG['OOPS'])}
            return HttpResponse(simplejson.dumps(return_data))
    data = {'form':form,'menu_obj':menu_obj}  
    cache.clear()      
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required    
def update_footer_positions(request):
    ''' method for updating orders of footer items '''
    #list[60]=root,list[58]=60,list[54]=root,list[55]=root,list[56]=root,list[57]=root,list[53]=root,list[59]=root,list[71]=root,list[73]=root
    data = request.GET['sortlist'].split(',')
    return_data = {}
    try:
        for position,menu_item in enumerate(data):
            menu, parent = menu_item.split('=')
            menu_obj = AvailableModules.objects.get(id=int(menu[5:-1]))
            if parent == 'root':
                menu_obj.parent = None
                menu_obj.level = 'footer'
            else:
                menu_obj.parent = AvailableModules.objects.get(id=int(parent))
                menu_obj.level = 'sub-footer'
            menu_obj.order = position
            menu_obj.save()
        return_data = {'msg':str(DESIGN_MSG['FMOS']),'mtype':get_msg_class_name('s')}
    except:
        return_data = {'msg':str(DESIGN_MSG['OOPS']),'mtype':get_msg_class_name('e')}
    cache.clear()
    return HttpResponse(simplejson.dumps(return_data))
    
         