from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils import simplejson
from django.contrib import messages

from common.templatetags.ds_utils import get_msg_class_name
from common.static_msg import PAGE_MSG
from common.pageform import PagesForm
from common.models import Pages
from common.getunique import getUniqueValue

from usermgmt.decorators import admin_required
from bs4 import BeautifulSoup

@admin_required
def edit_resources(request, id, template='default/common/edit_resources.html'):
    data = {}
    try:
        page = Pages.objects.get(id=id)
    except:
        if id == '0':
            page = False
        else:
            raise Http404
    data['page'] = page
    if request.method == "POST":
        content = request.POST['content'].strip()
        soup = BeautifulSoup(content)
        title = soup.find(name='h1', attrs={'id': 'title'})
        desc = soup.find(name='div', attrs={'id': 'page-body'})
        if page:
            slug = getUniqueValue(Pages, slugify(title.text), instance_pk=page.id)
        else:
            slug = getUniqueValue(Pages, slugify(title.text))
        if not page:
            page = Pages(
                modified_by = request.user,
                is_active = True
            )
        page.name = title.text
        page.seo_title = title.text.strip()[:70]
        page.seo_description = desc.text.strip()[:160]
        if not page.is_static:
            page.slug = slug
        page.content = content
        page.save()
        return HttpResponse('/%s.html' % (page.slug))
    else:
        return render_to_response(template, data, context_instance=RequestContext(request))

from common.fileupload import upload_photos_forgallery
from gallery.models import Photos

@admin_required
def resources_image_upload(request):
    if request.method == "POST":
        response = upload_photos_forgallery(request, Photos, None, 'album')
        return response
    
@admin_required    
def page(request,id,template='admin/portal/pages/page.html'):
    current_page=Pages.objects.get(id=id)
    form=PagesForm(instance=current_page)
    if request.method=='POST':
        form=PagesForm(request.POST,instance=current_page)
        if form.is_valid():
            page=form.save(commit=False)
            if not current_page.is_static:
                if id:page.slug=getUniqueValue(Pages,slugify(page.slug),instance_pk=page.id)
                else:page.slug=getUniqueValue(Pages,slugify(page.slug))
                page.slug = slugify(page.slug)
            else:
                page.slug = slugify(current_page.slug)
            page.modified_by=request.user
            page.save()
            return HttpResponseRedirect(reverse('admin_page_view',args=[page.id])+'?msg=PUS&mtype=s')
    data={'form':form,'nav_pages':Pages.objects.filter(is_static=True).order_by('name')}
    data['current_page']=current_page
    try:messages.success(request, str(PAGE_MSG[request.GET['msg']]))
    except:pass 
    return render_to_response (template, data, context_instance=RequestContext(request))   
    
@admin_required    
def custom_page(request,template='admin/portal/pages/custom.html'):
    data={
          'pages':Pages.objects.filter(is_static=False).order_by('name'),
          'custom_pages':Pages.objects.filter(is_static=False).order_by('name'),
          'custom_page':True,
          #'nav_pages':Pages.objects.filter(is_static=True).order_by('name')
    }
    
    try:messages.success(request, str(PAGE_MSG[request.GET['msg']]))
    except:pass 
    data['is_static_page'] = True
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required    
def custom_page_update(request,id=False,template='admin/portal/pages/custom_update.html'):
    if id:
        try:current_page=Pages.objects.get(id=id)
        except:raise Http404
        form=PagesForm(instance=current_page)
    else:form=PagesForm()
    if request.method=='POST':
        if id:form=PagesForm(request.POST,instance=current_page)
        else:form=PagesForm(request.POST)
        if form.is_valid():
            page=form.save(commit=False)
            if id:
                if not current_page.is_static:
                    page.slug = getUniqueValue(Pages, slugify(page.slug), instance_pk=page.id)
            else:page.slug = getUniqueValue(Pages, slugify(page.slug))
            page.slug = slugify(page.slug)
            page.modified_by=request.user
            page.save()
            return HttpResponseRedirect(reverse('admin_custom_page')+'?msg=CPUS&mtype=s')
    data={'form':form,'nav_pages':Pages.objects.filter(is_static=True).order_by('name')}
    if id:
        data['current_page']=current_page
        data['custom_page']=not current_page.is_static
    try:
        data['msg']=PAGE_MSG[request.GET['msg']]
        data['mtype']=get_msg_class_name(request.GET['mtype'])
    except:pass
    data['is_static_page'] = True
    return render_to_response (template, data, context_instance=RequestContext(request)) 

@admin_required
def custom_page_delete(request):
    send_data = {}
    try:
        page = Pages.objects.get(id=request.POST['page_id'])
        page.delete()
        send_data['status'] = 1
    except:
        send_data['status'] = 0
    return HttpResponse(simplejson.dumps(send_data))
        
@admin_required
def custom_page_statusss(request):
    try:
        page = Pages.objects.get(id=int(request.GET['id']))
        if page.is_active:page.is_active=False
        else:page.is_active=True
        page.save()
        status=1 
        msg=PAGE_MSG['PSCS']
        mtype='s'
    except:
        status=0
        msg=PAGE_MSG['OOPS']
        mtype='e'
    data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return HttpResponse(simplejson.dumps(data))

@admin_required
def custom_page_status(request):
    send_data={}
    try:
        page = Pages.objects.get(id=int(request.GET['id']))
        if page.is_active:
            page.is_active=False
            send_data['status_class']='icon-inactive-user' 
            send_data['status_text']='Active'
        else:
            page.is_active=True  
            send_data['status_class']='icon-active-user'
            send_data['status_text']='Inactive'  
        page.save()
        send_data['success']=True
    except:send_data['success']=False
    return HttpResponse(simplejson.dumps(send_data))