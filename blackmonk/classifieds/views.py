from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Q
from django.utils import simplejson
from common.models import ModuleNames
from common.utils import ds_pagination, contactemail_save
from django.conf import settings as my_settings

from classifieds.models import Classifieds,ClassifiedCategory,ClassifiedAttribute,ClassifiedAttributevalue
from usermgmt.favoriteviews import add_remove_fav,get_fav

NUMBER_DISPLAYED=12

def classified_home(request):
    data={}
    data['seo'] = ModuleNames.get_module_seo(name='classifieds')
    data['featured_classified']= Classifieds.objects.filter(status='P',listing_type='F',listing_end_date__gte=date.today()).select_related('created_by','album').order_by('-published_on')[:18]
    data['newclassifieds']= Classifieds.objects.filter(status='P').select_related('category','created_by','album').order_by('-published_on')[:6]
    data['categories']=ClassifiedCategory.objects.filter(parent__isnull=True).prefetch_related('parentcategory').order_by('name')
    return render_to_response('default/classifieds/categorylist.html',data,context_instance=RequestContext(request))  
    

def classified_listing(request,catslug=False):
    view_type = request.GET.get('view','grid')
    try:search = request.REQUEST['search']
    except:search = False
    if catslug:
        data = classifieds_filter(request,catslug,search)
        try:
            category_attr= data['category']
            data['attributes']= ClassifiedAttribute.objects.filter(Q(type='S')|Q(type='K')|Q(type='R'),Q(category = category_attr)|Q(category = category_attr.parent)).prefetch_related().order_by('-name')
        except:pass 
        data['categories']=ClassifiedCategory.objects.filter(parent__isnull=True).prefetch_related('parentcategory').order_by('name')
        data['view_type'] = view_type
        try:
            pcat = ClassifiedCategory.objects.get( slug = catslug )
            data['subcategories'] = ClassifiedCategory.objects.filter(parent = pcat.id).prefetch_related('parentcategory').order_by('name')
        except:pass
        return render_to_response('default/classifieds/classifiedlist.html',data, context_instance=RequestContext(request))
    elif search:
        try:
            cats=ClassifiedCategory.objects.get(id=request.GET['category'])
            cat=cats.slug
        except:
            cat=False
            cats=False
        data=classifieds_filter(request,cat,search)
        data['view_type'] = view_type
        data['seo'] = ModuleNames.get_module_seo(name='classifieds')
        data['categories']=ClassifiedCategory.objects.filter(parent__isnull=True).prefetch_related('parentcategory').order_by('name')
        if cat:data['search_cat']=cats
        try:
            category_attr= data['category']
            data['attributes']= ClassifiedAttribute.objects.filter(Q(type='S')|Q(type='K')|Q(type='R'),Q(category = category_attr)|Q(category = category_attr.parent)).prefetch_related().order_by('-name')
        except:pass 
        return render_to_response('default/classifieds/classifiedlist.html',data, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('classified_home'))
    
    
    
def classifieds_filter(request,catslug,search):
    key={}
    q=''
    q_text=()
    at_id=False
    val=False
    sort=request.REQUEST.get('srt',False)
    if sort=='hl':srt='-classified_price'
    elif sort=='lh':srt='classified_price'
    elif sort=='re':srt='-published_on'
    elif sort=='ol':srt='published_on'
    else:srt='-published_on'
    key['status'] = 'P'
    try:
        fp = int(request.GET['fp'])
        tp = int(request.GET['tp'])
        if fp!='' and tp!='':
            key['classified_price__range']=(fp,tp)
    except:
        fp=False
        tp=False
    
    if search:
        try:
            q = request.GET.get('find','')
            if not q:q = request.GET['q']
            q_text=(Q(title__icontains=q)|Q(description__icontains=q)|Q(category__name__icontains=q)|Q(category__parent__name__icontains=q)|Q(tags__tag__icontains=q))
        except:pass
        
    if catslug:
        try:selectedcat = ClassifiedCategory.objects.prefetch_related('parentcategory').get(slug=catslug)
        except:return HttpResponseRedirect(reverse('classified_home'))
        
        if selectedcat.parent:
            parent = False
            subcat = ClassifiedCategory.objects.filter(slug=catslug)
            subcategories = ClassifiedCategory.objects.filter(parent=selectedcat.parent)
        else:
            parent = True
            subcat = ClassifiedCategory.objects.filter(parent=selectedcat)
            subcategories = subcat
        key['category__in']=subcat
        try:
            subcatcount = int(round(subcategories.count()/4.0))
            if subcatcount==0:subcatcount=1
        except:subcatcount =1
        try:
            at_id=request.GET['at_id']
            val=request.GET['val']
            atr = ClassifiedAttribute.objects.get(id=at_id)
            if atr.type=='K':
                cls = ClassifiedAttributevalue.objects.filter(attribute_id__id=at_id,value__icontains=val,classified__status='P')
            else:
                cls = ClassifiedAttributevalue.objects.filter(attribute_id__id=at_id,value__iexact=val,classified__status='P')
            array_cls=[]
            for c in cls:array_cls.append(c.classified.id)
            key['id__in']=array_cls
        except:
            pass
    
    if q_text:
        classifiedsall = Classifieds.objects.filter(q_text,**key).prefetch_related('category').select_related('payment').distinct().order_by('-listing_type',srt)
    else:
        classifiedsall = Classifieds.objects.filter(**key).prefetch_related('category').distinct().select_related('payment').order_by('-listing_type',srt)
    
    
    try:page = int(request.GET['page'])
    except:page = 1
    data = ds_pagination(classifiedsall,page,'classifiedlist',NUMBER_DISPLAYED)
    data['classifiedsall']=classifiedsall
    if catslug:
        data['category']= selectedcat
        data['subcat']= subcategories
        data['parent']= parent
        data['seo'] = selectedcat
        data['subcatcount']=subcatcount
    if search:
        data['search'] = True
        data['q'] = q
        cat_ids=classifiedsall.values_list('category').distinct('id')
        data['search_category']=ClassifiedCategory.objects.filter(id__in=cat_ids).order_by('name')
    data['val'] = val
    data['at_id']=at_id
    data['fp']=fp
    data['tp']=tp
    data['sort']=sort
    return data


def classified_detail(request,slug):
    data={}
    try: 
        data['classified']=classified = Classifieds.objects.prefetch_related('category').select_related('payment').get(slug=slug,status='P')
        try:
            if request.session['classifiedview%s'%(classified.id)] != classified.id:
                request.session['classifiedview%s'%(classified.id)] = classified.id
                classified.most_viewed = classified.most_viewed + 1
                classified.save()
        except:
            try:
                request.session['classifiedview%s'%(classified.id)] = classified.id 
                classified.most_viewed = classified.most_viewed + 1
                classified.save()
            except:pass
    except:
        return HttpResponseRedirect(reverse('classified_home'))
    
    data['attrvalus'] = ClassifiedAttributevalue.objects.filter(classified = classified)
    data['relatedclass'] = Classifieds.objects.filter(Q(is_active=True),Q(status='P'),Q(category=classified.category)|Q(title__icontains=classified.title)|Q(description__icontains=classified.description)).exclude(id=classified.id)[:5]
    data['category'] = ClassifiedCategory.objects.filter(parent__isnull=True).order_by('id')
    data['categories']=ClassifiedCategory.objects.filter(parent__isnull=True).prefetch_related('parentcategory').order_by('name')
    #data['object_id'] = classified.id
    #data['content_type'] = 'classifieds'
    #data['suggested_item'] = classified
    #data['suggested_by'] = request.user.profile.display_name.title()
        
    return render_to_response('default/classifieds/classifieddetail.html',data, context_instance=RequestContext(request))

def classified_count(request,id):
    try:
        classified = Classifieds.objects.get(id=id)
        classified.most_viewed = classified.most_viewed + 1
        classified.save()
        return HttpResponse('1')
    except:return HttpResponse('0')

def tp_classified(request,id,template='default/classifieds/tp_classified_detail.html'):
    classified = get_object_or_404(Classifieds, tp_id=id)
    categorytype = ClassifiedCategory.objects.filter(parent__isnull=True).order_by('id')
    return render_to_response(template,locals(),context_instance=RequestContext(request))

def contact(request):
    data={}
    if request.method == 'POST':
        try:
            classifieds = Classifieds.objects.get(id=int(request.REQUEST['cid']))
            contactemail_save(request, classifieds)

            from common.utils import get_global_settings
            global_settings = get_global_settings()
            subject = global_settings.domain+" | "+classifieds.title
            to_emailids = [classifieds.address.email]
            data={"Name": request.POST['respond_name'],"Email":request.POST['respond_email'],"Phone":request.POST['respond_phone'],"Subject": request.POST['respond_msg']}
            email_message = render_to_string("default/classifieds/mail_msg.html", data,context_instance=RequestContext(request))
            email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL, to_emailids)
            email.content_subtype = "html"
            email.send()
            
            return HttpResponse('1')
        except:
            pass
    else:
        data['classified'] = Classifieds.objects.get(id=int(request.REQUEST['cid']))
        return render_to_response("default/classifieds/contact_from.html",data,context_instance=RequestContext(request))
    
   

def ajax_tell_a_friend(request):
    scaptcha = {}
    from common.utils import get_global_settings
    global_settings = get_global_settings()
    if request.method == 'POST':
        clas = Classifieds.objects.get(id=request.POST['content_id'])
        from_name = request.POST['from_name']
        to_name = request.POST['to_name']
        to_email = request.POST['to_email']
        msg = request.POST['msg']
        subject = global_settings.domain + ' - '+from_name+' sent you the details of a Classified Ad "'+clas.title+' "'
        
        tell_a_friend_data = {}
        tell_a_friend_data['from_name'] = from_name
        tell_a_friend_data['to_name'] = to_name
        tell_a_friend_data['to_email'] = to_email
        tell_a_friend_data['subject'] = subject
        tell_a_friend_data['msg'] = msg
        tell_a_friend_data['classified'] = clas
        email_message = render_to_string("default/classifieds/sendtofriend.html",tell_a_friend_data,context_instance=RequestContext(request))
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,[to_email])
        email.content_subtype = "html"
        email.send()
        scaptcha['success'] = 1
        data  = simplejson.dumps(scaptcha)
        return HttpResponse(data)
    scaptcha['success'] = 0
    data  = simplejson.dumps(scaptcha)
    return HttpResponse(data)
    
   
def auto_suggest_classifieds(request):
    try:
        q=request.POST['query']
        q_key=(Q(title__icontains=q)|Q(description__icontains=q)|Q(category__name__icontains=q)|Q(category__parent__name__icontains=q)|Q(tags__tag__icontains=q))
        data = Classifieds.objects.filter(q_key,status='P').distinct()[:10]
    except:
        data = False
    child_dict = []
    if data:
        for cls in data :
            buf={'id':cls.id,'name':cls.title}
            child_dict.append(buf)
    return HttpResponse(simplejson.dumps(child_dict), content_type="application/json")

def classifieds_add_to_fav(request):
    try:
        classified = Classifieds.objects.get(id=request.GET['id'],status='P')
        flag=add_remove_fav(classified,request.user)
        return HttpResponse(flag)
    except:return HttpResponse('0')  
    