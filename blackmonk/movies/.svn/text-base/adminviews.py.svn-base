#Python

#Django
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.db.models import Count

#Library
from common.static_msg import MOVIES_MSG
from common.admin_utils import success_response_to_save_genre_lang,error_response,response_delete_genre_lang,response_to_save_settings
from common.templatetags.ds_utils import get_msg_class_name
from common.getunique import getUniqueValue
from common.models import ModuleNames
from common.forms import SEOForm
from usermgmt.decorators import admin_required

from movies.models import MovieType,MovieLanguage,Theatres,Movies,CriticSource
from movies.forms import MovieTypeForm,MovieTypeSEOForm,MovieLanguageForm,AddCriticsSource


"""
#####################################################################################################################
##############################################        MOVIES       #################################################
#####################################################################################################################
"""
@admin_required
def movies_settings(request, template='admin/portal/movies/settings.html'):
    active=inactive=featured=0
    
    moviestype=MovieType.objects.all().count()
    theatres=Theatres.objects.all().count()
    langauge=MovieLanguage.objects.all().count()
    movies_state = Movies.objects.values('is_active').annotate(a_count=Count('is_active'))
    criticsource=CriticSource.objects.all().count()
    
    for st in movies_state:
        if st['is_active']:
            active+=st['a_count']
        else:
            inactive+=st['a_count']
        
    
    data={
          'movies':active+inactive,
          'active_movies':active,
          'inactive_movies':inactive,
          'langauge':langauge,
          'theatres':theatres,
          'genre':moviestype,
          'criticsource':criticsource
    }
    
    try:seo = ModuleNames.get_module_seo(name='movies')
    except:seo = ModuleNames(name='movies')        
    if request.method=='POST':
        seo_form = SEOForm(request.POST)
        if seo_form.is_valid(): 
            seo.seo_title = seo_form.cleaned_data.get('meta_title')
            seo.seo_description = seo_form.cleaned_data.get('meta_description')
            seo.modified_by = request.user
            seo.save()
            extra_data = {'seo':seo,'seo_form':seo_form}
            data.update(extra_data)
            return response_to_save_settings(request,True,data,'admin/portal/movies/include_settings.html',MOVIES_MSG)
        else:
            extra_data = {'seo':seo,'seo_form':seo_form}
            data.update(extra_data)
            return response_to_save_settings(request,False,data,'admin/portal/movies/include_settings.html',MOVIES_MSG)

    data['seo'] = seo
    return render_to_response (template, data, context_instance=RequestContext(request))




################################################## GENRE #####################################################

@admin_required
def movies_genre(request, template='admin/portal/movies/genre.html'):
    category=MovieType.objects.order_by('name')
    data={'category':category}
    try:data['msg']=MOVIES_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def movies_genre_update(request,template='admin/portal/movies/update_genre.html'):
    data={}
    cat=None
    try:
        cat = MovieType.objects.get(id=request.REQUEST['id'])
        form = MovieTypeForm(instance=cat)
    except:form = MovieTypeForm()
    if request.method=='POST':
        if cat:form = MovieTypeForm(request.POST,instance=cat)
        else:form = MovieTypeForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            if category.slug:category.slug = getUniqueValue(MovieType,slugify(form.cleaned_data.get('slug')),instance_pk=category.id)
            else:category.slug = getUniqueValue(MovieType,slugify(form.cleaned_data.get('name')),instance_pk=category.id)
            category.created_by = category.modified_by = request.user
            category.is_active = True
            category.save()
            form=MovieTypeForm()
            data = {'form':form,'cat':cat}
            append_data={'cat':category,'edit_url':reverse('admin_portal_movies_genre_update')}
            return success_response_to_save_genre_lang(append_data,data,template,MOVIES_MSG)
        else:
            data = {'form':form,'cat':cat}
            return error_response(data,template,MOVIES_MSG)
    else:
        data = {'form':form,'cat':cat}
        return render_to_response(template,data,context_instance=RequestContext(request))
        
@admin_required
def movies_genre_delete(request):
    data=response_delete_genre_lang(request,MovieType,MOVIES_MSG)
    return HttpResponse(simplejson.dumps(data))

################################################## CRICTIC SOURCT #####################################################

@admin_required
def movies_criticsource(request, template='admin/portal/movies/criticsource.html'):
    category=CriticSource.objects.order_by('source_title')
    data={'category':category}
    try:data['msg']=MOVIES_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def movies_criticsource_update(request,template='admin/portal/movies/update_criticsource.html'):
    data={}
    cat=None
    try:
        cat = CriticSource.objects.get(id=request.REQUEST['id'])
        form = AddCriticsSource(instance=cat)
    except:form = AddCriticsSource()
    if request.method=='POST':
        if cat:form = AddCriticsSource(request.POST,instance=cat)
        else:form = AddCriticsSource(request.POST)
        if form.is_valid():
            category = form.save()
            form=AddCriticsSource()
            data = {'form':form,'cat':cat}
            append_data={'cat':category,'edit_url':reverse('admin_portal_movies_criticsource_update')}
            return success_response_to_save_genre_lang(append_data,data,template,MOVIES_MSG,'C')
        else:
            data = {'form':form,'cat':cat}
            return error_response(data,template,MOVIES_MSG)
    else:
        data = {'form':form,'cat':cat}
        return render_to_response(template,data,context_instance=RequestContext(request))
        
@admin_required
def movies_criticsource_delete(request):
    data=response_delete_genre_lang(request,CriticSource,MOVIES_MSG,'C')
    return HttpResponse(simplejson.dumps(data))
################################################## LANGUAGE #########################################

@admin_required
def movies_language(request, template='admin/portal/movies/langauge.html'):
    category=MovieLanguage.objects.order_by('name')
    data={'category':category}
    try:data['msg']=MOVIES_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def movies_language_update(request,template='admin/portal/movies/update_language.html'):
    try:
        data={}
        cat=None
        try:
            cat = MovieLanguage.objects.get(id=request.REQUEST['id'])
            form = MovieLanguageForm(instance=cat)
        except:form = MovieLanguageForm()
        if request.method=='POST':
            if cat:form = MovieLanguageForm(request.POST,instance=cat)
            else:form = MovieLanguageForm(request.POST)
            if form.is_valid():
                category = form.save()
                form=MovieLanguageForm()
                data = {'form':form,'cat':cat}
                append_data={'cat':category,'edit_url':reverse('admin_portal_movies_language_update')}
                return success_response_to_save_genre_lang(append_data,data,template,MOVIES_MSG,'L')
            else:
                data = {'form':form,'cat':cat}
                return error_response(data,template,MOVIES_MSG)
        else:
            data = {'form':form,'cat':cat}
            return render_to_response(template,data,context_instance=RequestContext(request))
    except:return HttpResponse(str(MOVIES_MSG['OOPS']))
        
@admin_required
def movies_language_delete(request):
    data=response_delete_genre_lang(request,MovieLanguage,MOVIES_MSG,'L')
    return HttpResponse(simplejson.dumps(data))

@admin_required
def movies_seo_genre_update(request, template='admin/portal/movies/update_genre_seo.html'):
    try:
        try:seo = MovieType.objects.get(id=int(request.REQUEST['id']))
        except:return HttpResponse(str(MOVIES_MSG['GNF']))
        form=MovieTypeSEOForm(instance=seo)
        if request.method=='POST':
            form = MovieTypeSEOForm(request.POST,instance=seo)
            if form.is_valid():
                seo=form.save(commit=False)
                try:seo.slug = getUniqueValue(MovieType,slugify(request.POST['slug']),instance_pk=seo.id)
                except:seo.slug = getUniqueValue(MovieType,slugify(seo.name),instance_pk=seo.id)
                seo.save()
                data={'status':1,'msg':str(MOVIES_MSG['GSUS']),'mtype':get_msg_class_name('s')}
                return HttpResponse(simplejson.dumps(data))
            else:
                data = {'form':form,'seo':seo}
                return error_response(data,template,MOVIES_MSG)
        data={'seo':seo,'form':form}
        return render_to_response (template, data, context_instance=RequestContext(request))
    except:return HttpResponse(str(MOVIES_MSG['OOPS']))


