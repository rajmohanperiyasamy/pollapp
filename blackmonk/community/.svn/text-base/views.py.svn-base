from django.shortcuts import render_to_response,get_object_or_404,HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template import RequestContext
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.core.mail import EmailMessage
from django.conf import settings as my_settings
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from common.utils import ds_pagination, get_global_settings
from common.getunique import getUniqueValue
from common.models import ModuleNames, ApprovalSettings
from community.models import Topic, Entry
from community.utils import set_answer_ratings
from common.mail_utils import mail_publish_community
#from community.forms import AddQnaForm
from community.forms import AddEntryForm
from usermgmt.favoriteviews import add_remove_fav
from common import signals

from common.models import CommentSettings  
from mptt_comments.models import MpttComment
from mptt_comments.forms import MpttCommentForm
from django.views.decorators.http import require_POST
from django.db import models
from django.contrib.comments import signals as signals1

import datetime
from datetime import date,timedelta


NUMBER_DISPLAYED = 12

def community_listing(request,type="top_stories"):
    data = topic_data = {}
    #######common###############
    try:page=int(request.GET['page'])
    except:page=1
    search = request.GET.get('src',False)
    filter_by = request.GET.get('filter_by','year')
    qu = request.GET.get('kw','')
    if search:
        try:
            ans=Entry.objects.filter(content__icontains=qu,entry_type='A').values_list('id', flat=True)
            if ans:
                q=(Q(title__icontains=qu)|Q(content__icontains=qu)|Q(topic__name__icontains=qu)|Q(id__in=ans))
            else:
                q=(Q(title__icontains=qu)|Q(content__icontains=qu)|Q(topic__name__icontains=qu))
        except:ans=q=qu=None
    else:ans=q=qu=None
    
    topics = Topic.objects.all().order_by('name')
    
    key={'status':'P'}
    ######common###############
    
    if type=="top_stories":
        if q:entry_list = Entry.objects.filter(q,**key).order_by('-created_on') 
        else:entry_list = Entry.objects.filter(**key).order_by('-created_on') 
    elif type=="question_answer":
        if q:entry_list = Entry.objects.filter(q,**key).exclude(entry_type="P").order_by('-created_on')
        else:entry_list = Entry.objects.filter(**key).exclude(entry_type="P").order_by('-created_on')
    elif type=="open_question":
        if q:entry_list = Entry.objects.filter(q,entry_type='Q',**key).order_by('-created_on')
        else:entry_list = Entry.objects.filter(entry_type='Q',**key).order_by('-created_on')
        answered_qlist = Entry.objects.exclude(question=None).values_list('question__id')
        entry_list = entry_list.exclude(id__in=answered_qlist)
    elif type=="posts":
        if q:entry_list = Entry.objects.filter(q,entry_type='P',**key).order_by('-created_on')
        else:entry_list = Entry.objects.filter(entry_type='P',**key).order_by('-created_on')
    else:
        if q:entry_list = Entry.objects.filter(q,topic__slug=type,**key).order_by('-created_on')
        else:entry_list = Entry.objects.filter(topic__slug=type,**key).order_by('-created_on')
        topic=Topic.objects.get(slug=type)
        topic_data['topic_selected'] = topic
        topic_data['topic_status'] = request.user in data['topic_selected'].subscriber.all()
        topic_data['followers'] = data['topic_selected'].subscriber.all().count()
    
    if filter_by and not search:
        today=datetime.datetime.now()
        if filter_by == 'week':
            week=today-timedelta(7)
            entry_list = entry_list.filter(created_on__range=(week,today)).order_by('-created_on')
            topic_data['filter_by'] = 'week'
        elif filter_by == 'month':
            month=today-timedelta(30)
            entry_list = entry_list.filter(created_on__range=(month,today)).order_by('-created_on')
            topic_data['filter_by'] = filter_by
        elif filter_by == 'year':
            year=today-timedelta(365)
            entry_list = entry_list.filter(created_on__range=(year,today)).order_by('-created_on')
            topic_data['filter_by'] = filter_by
        
    
    data = ds_pagination(entry_list,page,'entries',NUMBER_DISPLAYED)
    data.update(topic_data)
    #data['url'] = url
    data['seo'] = ModuleNames.get_module_seo(name='community')
    data['topics'] = topics
    data['type'] = type 
    data['q'] = qu
    data['kw'] = qu
    data['search'] = search
    
    return render_to_response('default/community/home.html',data, context_instance=RequestContext(request))

def add_entry(request):
    data = {}
    add_type = request.REQUEST.get('add_type','')
    topics = Topic.objects.all().order_by('name')
    id = request.GET.get('id')
    type = request.GET.get('type')
    if add_type == "qna":
        template='default/community/qna_form.html'
    else:
        template='default/community/add_post.html'
    if id:
        entry = Entry.objects.get(id = id)
        form = AddEntryForm(instance=entry)
    else:
        form = AddEntryForm()
        entry = False
    if request.POST:
        if id:
            form = AddEntryForm(request.POST,instance=entry)
        else:
            form = AddEntryForm(request.POST)
        send_data={}
        if form.is_valid():
            entry_form = form.save(commit = False)
            entry_form.slug = getUniqueValue(Entry,slugify(entry_form.title),instance_pk = entry_form.id)
            entry_form.created_by = entry_form.modified_by = request.user
            if add_type == 'qna':
                entry_form.entry_type = "Q"
            else:
                entry_form.entry_type = "P"
            approval_settings=ApprovalSettings.objects.get(name='community')
            if approval_settings.free:
                entry_form.status = 'P'
            else:
                entry_form.status = 'P'#Change to N
            entry_form.save()
            entry_form.subscriber.add(request.user)
            mail_publish_community(entry_form)
            signals.celery_update_index.send(sender=None,object=entry_form)
            if entry:
                signals.create_staffmail.send(sender=None,object=entry_form,module='community',action='U',user=request.user)
            else:
                signals.create_staffmail.send(sender=None,object=entry_form,module='community',action='A',user=request.user)
            signals.create_notification.send(sender=None,user=request.user, obj=entry_form, not_type='(question) added in',obj_title=entry_form.question)
            send_data['status'] = 1
            if add_type == "qna":
                send_data['url'] = entry_form.get_absolute_url()
                return HttpResponse(simplejson.dumps(send_data))
            else:
                return HttpResponseRedirect(reverse('community_listing', args=["top_stories"]))
        elif add_type == "qna":
            data['form']=form
            data['topics'] = topics
            send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps(send_data))
        
    data['topics'] = topics
    data['form'] = form
    return render_to_response(template, data, context_instance=RequestContext(request))

def entry_detail(request, top, slug):
    data = {}
    try:
        entry = Entry.objects.get(slug=slug,topic__slug=top)
    except:
        return HttpResponseRedirect(reverse('community_listing'))
    topics = Topic.objects.all().order_by('name')
    
    answers = Entry.objects.filter(entry_type='A',question__id=entry.id).order_by('-created_on')
    if slug:
        ques=Entry.objects.get(slug=slug)
        if request.user in ques.subscriber.all():
            data['entry_status'] = True
        else:
            data['entry_status'] = False
    if answers:
        data['answers']=answers
    data['topics']=topics
    data['entry']=entry
    return render_to_response('default/community/entry-detail.html',data, context_instance=RequestContext(request))

@login_required
def save_answer(request,id,template="default/community/answer_form.html"):
    data = {}
    entry=get_object_or_404(Entry,id=id)
    #entry=Entry.objects.get(id=id)
    aid = request.GET.get("aid")
    if aid:
        answer = Entry.objects.get(id=aid)
    else:
        answer=False
    
    if request.POST:
        try:
            if aid:
                ans = Entry.objects.get(id=aid,created_by=request.user)
                ans.content = request.POST['answer']
            else:
                ans = Entry(content = request.POST['answer'],question = entry,created_by=request.user)
            ans.entry_type='A'
            ans.title=entry.title
            try:
                entry.objects.get(subscriber = request.user,id=id)
            except:
                entry.subscriber.add(request.user)
            approval_settings=ApprovalSettings.objects.get(name='community')
            if approval_settings.paid:ans.status = 'P'
            else:ans.status = 'P'#Change to N
            ans.topic=entry.topic
            ans.save()
            mail_publish_community(ans)
            signals.celery_update_index.send(sender=None,object=ans)
            if answer:
                signals.create_staffmail.send(sender=None,object=ans,module='community',action='U',user=request.user)
            else:
                signals.create_staffmail.send(sender=None,object=ans,module='community',action='A',user=request.user)
            signals.create_notification.send(sender=None,user=request.user, obj=ans, not_type='answer added for this question in',obj_title=ans.question)
            return HttpResponseRedirect('/community/%s/%s.html#id_answ_%s'%(entry.topic.slug,entry.slug,ans.id))
        except:
            return HttpResponseRedirect('/community/%s/%s.html'%(entry.topic.slug,entry.slug)+'?msg=nar')
    data["answer"] = answer
    data["entry"] = entry    
    return render_to_response(template, data, context_instance=RequestContext(request))

def ajax_viewed(request,id):
    entry=Entry.objects.get(id=id)
    try:
        if request.session['views%s'%(entry.id)] != entry.id:
            request.session['views%s'%(entry.id)] = entry.id
            entry.viewed=entry.viewed+1
            entry.save()
    except:
        request.session['views%s'%(entry.id)] = entry.id
        entry.viewed=entry.viewed+1
        entry.save()
    return HttpResponse('1') 


def load_comment(request,objid):
    data = {}
    send_data = {}
    entry = Entry.objects.get(id=objid,entry_type='A')
    template = 'default/community/comments/load_comment.html'
    data['entry']=entry
    send_data['display_html']=render_to_string(template, data, context_instance=RequestContext(request))
    return HttpResponse(simplejson.dumps(send_data))

def community_replay_comment(request, comment_id=None):
    try:
        comment_id = request.POST['c_id']
        parent_comment = get_object_or_404(MpttComment, pk=comment_id)
        target = parent_comment.content_object
        model = target.__class__
        form = MpttCommentForm(target, parent_comment=parent_comment)
        
        if request.user.is_authenticated():user = request.user
        else:user = None
        
        data = {"form":form,"user":user,"object":target,"comment_id":comment_id}
        display_html=render_to_string('default/community/comments/replay_form.html',data,context_instance=RequestContext(request))
        send_data={'display_html':display_html,'status':'success'}
    except:
        send_data={'status':'fail'}
    return HttpResponse(simplejson.dumps(send_data))

def community_load_parent_comment(request):
    try:
        comment = MpttComment.objects.get(pk=int(request.POST['parent_id']),is_removed=False,is_public=True)
        data = get_all_comment_settings()
        data["comment"]=comment
        display_html=render_to_string('default/community/comments/load_parent_comment.html',data,context_instance=RequestContext(request))
        send_data={'html':display_html,'status':'success'}
    except:
        display_html=render_to_string('default/community/comments/load_parent_comment.html',{'comment':False},context_instance=RequestContext(request))
        send_data={'html':display_html,'status':'error'}
    return HttpResponse(simplejson.dumps(send_data))

def community_load_more_comment(request):
    try:
        ctype = request.POST.get("content_type")
        object_pk = request.POST.get("object_pk")
        model = models.get_model(*ctype.split(".", 1))
        target = model._default_manager.get(pk=object_pk)
        data = get_all_comment_settings()
        data["object"]=target
        data['page']=request.POST.get('page',2)
        display_html=render_to_string('default/community/comments/load_more_comment.html',data,context_instance=RequestContext(request))
        send_data={'display_html':display_html,'status':'success'}
    except:
        send_data={'status':'fail'}
    return HttpResponse(simplejson.dumps(send_data))


@require_POST
def community_post_comment(request):
    try:
        if request.method != 'POST':
            return http.HttpResponseNotAllowed(["POST"])
        data = request.POST.copy()
        reply=request.POST.get('reply',False)
        review = request.POST.get("review",False)
        if review == 'review':review=True
        else:review=False
        if request.user.is_authenticated():
            user = request.user
            data['email'] = user.useremail
            data['name'] = user.get_full_name()
        else:user = None
        data['title'] = ' '
        ctype = data.get("content_type")
        object_pk = data.get("object_pk")
        comment_id=parent_pk = data.get("parent_pk")
        review_flag=True
        if review:
            model = ctype.split(".")[1]
            try:
                comment=MpttComment.objects.get(content_type__model=model,object_pk=object_pk,user=request.user)
                review_flag=False
            except:
                review_flag=True
        if not review_flag:
            if data.get('ratings'):
                comment.rating=data.get('ratings')
            else:
                comment.rating=0.0
            comment.comment=data.get('comment')
            comment.save()
        if review_flag:
            parent_comment = None
            if ctype is None or object_pk is None:return HttpResponse(simplejson.dumps({'status':'err'}))
            try:
                model = models.get_model(*ctype.split(".", 1))
                target = model._default_manager.get(pk=object_pk)
                if parent_pk:
                    parent_comment = MpttComment.objects.get(pk=parent_pk)
            except TypeError:return HttpResponse(simplejson.dumps({'status':'err'}))
            except AttributeError:return HttpResponse(simplejson.dumps({'status':'err'}))
            except MpttComment.DoesNotExist:return HttpResponse(simplejson.dumps({'status':'err'}))
            except ObjectDoesNotExist:return HttpResponse(simplejson.dumps({'status':'err'}))
            form = MpttCommentForm(target, parent_comment=parent_comment, data=data)
            if form.security_errors():return HttpResponse(simplejson.dumps({'status':'err'}))
            form.email = request.user.useremail
            if form.errors:
                data = {"comment":form.data.get("comment", ""),"form":form,'reply':reply,'comment_id':comment_id, "object":target,"user":user,'review':review}
                form_html=render_to_string('default/community/comments/form.html',data,context_instance=RequestContext(request))
                send_data={'form_html':form_html,'status':'form_err'}
                return HttpResponse(simplejson.dumps(send_data))
            comment = form.get_comment_object(user)
            comment.ip_address = request.META.get("REMOTE_ADDR", None)
            if request.user.is_authenticated():
                comment.user = request.user
            responses = signals1.comment_will_be_posted.send(
                sender  = comment.__class__,
                comment = comment,
                request = request
            )
            for (receiver, response) in responses:
                if response == False:HttpResponse(simplejson.dumps({'status':'err'}))
            if data.get('ratings'):
                comment.rating=data.get('ratings')
            else:
                comment.rating=0.0
            comment.save()
            signals1.comment_was_posted.send(
                sender  = comment.__class__,
                comment = comment,
                request = request
            )
        try:
            if comment.content_type.model=='business' or comment.content_type.model=='movies' or comment.content_type.model=='restaurants':
                c_type=ContentType.objects.get_for_model(comment.content_object)
                buz=c_type.model_class().objects.get(id=comment.object_pk)
                comments=MpttComment.objects.filter(level__gte=1,content_type=c_type,object_pk=buz.id).exclude(rating=0)
                count=comments.count()
                if count:
                    total_sum=0
                    for c in comments:
                        if c.rating:total_sum+=c.rating 
                    if total_sum:buz.ratings=round(float(total_sum/count),1)
                    else:buz.ratings=0
                    buz.save()
        except:pass
        data = get_all_comment_settings()
        data["comment"]=comment
        data['msg']=1
        if not reply:template='default/community/comments/load_new_comment.html'
        else:template='default/community/comments/load_reply_comment.html'
        display_html=render_to_string(template,data,context_instance=RequestContext(request))
        send_data={'display_html':display_html,'status':'success','approved':comment.is_public,'comment__id':comment.id,'review_flag':review_flag}
        return HttpResponse(simplejson.dumps(send_data))
    except:
        send_data={'status':'form_err'}
        return HttpResponse(simplejson.dumps(send_data))

def get_all_comment_settings():
    data={}
    obj=CommentSettings.get_or_create_obj()
    data['cc_like_dislike'] = obj.like_dislike
    data['cc_flag'] = obj.flag
    data['cc_discuss_comment'] = obj.discuss_comment
    data['cc_threaded'] = obj.threaded
    data['cc_avatar'] = obj.avatar
    data['cc_rating'] = obj.rating
    data['cc_approval'] = obj.approval
    return data


def answer_user_rating(request):
    ''' calling method written utils for set like, dislike for particular answer'''
    data = set_answer_ratings(request)
    answer = Entry.objects.get(id = request.GET['aid'])
    if data["rating"] == 'like':
        data["function"] = "answer_response('%d','like','%s');" % (answer.id, reverse('answer_answer_user_rating'))
    elif data["rating"] == 'dislike':
        data["function"] = "answer_response('%d','dislike','%s');" % (answer.id,reverse('answer_answer_user_rating'))
    else:
        data["function"] = "answer_response('%d','like','%s');" % (answer.id,reverse('answer_answer_user_rating'))
    return HttpResponse(simplejson.dumps(data)) 



###################subscribers#####################################
@login_required  
def entry_follow(request,id):
    data = {}
    send_data = {}
    sl_template = 'default/community/subscribers_list.html'
    entry_status = False
    try:
        entry = Entry.objects.get(id=id)
        try: 
            entry.objects.get(subscriber = request.user,id=id)
            entry_status = True
        except:
            entry.subscriber.add(request.user)
            entry_status = True
        subscribers_list = entry.subscriber.all()
        data['entry'] = entry
        data['entry_status'] = entry_status
        data['subscribers_list'] = subscribers_list
        send_data['subscribers_html'] = render_to_string(sl_template, data, context_instance=RequestContext(request))    
        send_data['subscribers_count'] = subscribers_list.count()
        send_data['action'] = "Following"
        send_data['follow_class']="noclass"    
        send_data['status'] = True  
    except:
        send_data['status'] = False 
    send_data['function']="check_login('%d','unfollow');" % (entry.id)
    send_data['function2']="check_login('%d','unfollowques');" % (entry.id)
    return HttpResponse(simplejson.dumps(send_data))

@login_required  
def entry_unfollow(request,id):
    data = {}
    send_data = {}
    sl_template = 'default/community/subscribers_list.html'
    entry_status = False
    try:
        entry = Entry.objects.get(id=id)
        entry.subscriber.remove(request.user)
        entry_status = True
        subscribers_list = entry.subscriber.all()  
        data['entry'] = entry
        data['entry_status'] = entry_status
        data['subscribers_list'] = subscribers_list
        send_data['subscribers_html'] = render_to_string(sl_template, data, context_instance=RequestContext(request))    
        send_data['subscribers_count'] = subscribers_list.count()
        send_data['action'] = "Follow"
        send_data['follow_class']= "class"
        send_data['status'] = True  
    except:
        send_data['status'] = False 
    send_data['function']="check_login('%d','follow');"% (entry.id)
    send_data['function2']="check_login('%d','followques');"% (entry.id)
    return HttpResponse(simplejson.dumps(send_data))


@login_required  
def topic_follow(request,id):
    send_data = {}
    try:
        topic = Topic.objects.get(id=id)
        try:
            topic = Topic.objects.get(subscriber = request.user,id=id)
            send_data['followers'] = topic.subscriber.all().count()
        except:
            topic.subscriber.add(request.user)
            send_data['followers'] = topic.subscriber.all().count()
        send_data['status'] = True  
    except:
        send_data['status'] = False
    send_data['function']="check_login('{{topic.id}}','unsubtopic');"
    return HttpResponse(simplejson.dumps(send_data))


@login_required  
def topic_unfollow(request,id):
    send_data = {}
    try:
        topic = Topic.objects.get(subscriber = request.user,id=id)
        topic.subscriber.remove(request.user)
        send_data['followers'] = topic.subscriber.all().count()
        send_data['status'] = True 
    except:
        send_data['status'] = False  
    send_data['function']="check_login('{{topic.id}}','subtopic');"
    return HttpResponse(simplejson.dumps(send_data))
    












