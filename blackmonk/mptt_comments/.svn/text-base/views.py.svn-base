from __future__ import division
import textwrap

from django import http
from django.http import Http404,HttpResponse
from django.conf import settings
from django.contrib.comments.views.utils import next_redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import escape
from django.contrib.comments import signals
from django.utils import datastructures, simplejson
from django.views.decorators.cache import cache_page,cache_control
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST

from common.models import CommentSettings  
from mptt_comments.models import MpttComment
from mptt_comments.forms import MpttCommentForm
from business.models import Business

class CommentPostBadRequest(http.HttpResponseBadRequest):
    def __init__(self, why):
        super(CommentPostBadRequest, self).__init__()
        if settings.DEBUG:
            self.content = render_to_string("comments/400-debug.html", {"why": why})

def replay_comment(request, comment_id=None):
    try:
        comment_id = request.POST['c_id']
        parent_comment = get_object_or_404(MpttComment, pk=comment_id)
        target = parent_comment.content_object
        model = target.__class__
        form = MpttCommentForm(target, parent_comment=parent_comment)
        
        if request.user.is_authenticated():user = request.user
        else:user = None
        
        data = {"form":form,"user":user,"object":target,"comment_id":comment_id}
        display_html=render_to_string('comments/replay_form.html',data,context_instance=RequestContext(request))
        send_data={'display_html':display_html,'status':'success'}
    except:
        send_data={'status':'fail'}
    return HttpResponse(simplejson.dumps(send_data))

def load_parent_comment(request):
    try:
        comment = MpttComment.objects.get(pk=int(request.POST['parent_id']),is_removed=False,is_public=True)
        data = get_all_comment_settings()
        data["comment"]=comment
        display_html=render_to_string('comments/load_parent_comment.html',data,context_instance=RequestContext(request))
        send_data={'html':display_html,'status':'success'}
    except:
        display_html=render_to_string('comments/load_parent_comment.html',{'comment':False},context_instance=RequestContext(request))
        send_data={'html':display_html,'status':'error'}
    return HttpResponse(simplejson.dumps(send_data))

def load_more_comment(request):
    try:
        ctype = request.POST.get("content_type")
        object_pk = request.POST.get("object_pk")
        model = models.get_model(*ctype.split(".", 1))
        target = model._default_manager.get(pk=object_pk)
        data = get_all_comment_settings()
        data["object"]=target
        data['page']=request.POST.get('page',2)
        display_html=render_to_string('comments/load_more_comment.html',data,context_instance=RequestContext(request))
        send_data={'display_html':display_html,'status':'success'}
    except:
        send_data={'status':'fail'}
    return HttpResponse(simplejson.dumps(send_data))


@require_POST
def post_comment(request):
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
                form_html=render_to_string('comments/form.html',data,context_instance=RequestContext(request))
                send_data={'form_html':form_html,'status':'form_err'}
                return HttpResponse(simplejson.dumps(send_data))
            comment = form.get_comment_object(user)
            comment.ip_address = request.META.get("REMOTE_ADDR", None)
            if request.user.is_authenticated():
                comment.user = request.user
            responses = signals.comment_will_be_posted.send(
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
            signals.comment_was_posted.send(
                sender  = comment.__class__,
                comment = comment,
                request = request
            )
        try:
            if comment.content_type.model=='business' or comment.content_type.model=='product' or comment.content_type.model=='movies' or comment.content_type.model=='restaurants':
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
#         try:
#             if comment.content_type.model=='business':
#                 buz=Business.objects.get(id=comment.object_pk)
#                 c_type=ContentType.objects.get_for_model(buz)
#                 if c_type.model=='business':
#                     comments=MpttComment.objects.filter(level__gte=1,content_type=c_type,object_pk=buz.id).exclude(rating=0)
#                     count=comments.count()
#                     if count:
#                         total_sum=0
#                         for c in comments:
#                             total_sum+=c.rating
#                         a=round(float(total_sum/count),1)
#                         avg=str(a).split('.')
#                         avg[1]=int(avg[1])
#                         avg[0]=int(avg[0])
#                         if avg[1]==0:rating=avg[0]
#                         elif avg[1]>3 and avg[1]< 8:rating=avg[0]+.5
#                         else:rating=a+1
#                         buz.ratings=rating
#                         buz.save()
#         except:
#             pass
        data = get_all_comment_settings()
        data["comment"]=comment
        data['msg']=1
        if not reply:template='comments/load_new_comment.html'
        else:template='comments/load_reply_comment.html'
        display_html=render_to_string(template,data,context_instance=RequestContext(request))
        send_data={'display_html':display_html,'status':'success','approved':comment.is_public,'comment__id':comment.id,'review_flag':review_flag}
        return HttpResponse(simplejson.dumps(send_data))
    except:
        send_data={'status':'form_err'}
        return HttpResponse(simplejson.dumps(send_data))

def check_review(request,object_id,model):
    try:
        try:model=model.split('_')[0]
        except:pass
        MpttComment.objects.get(object_pk=object_id,user=request.user,content_type__model__iexact=model)
        return HttpResponse("1")
    except:return HttpResponse("0")
        

def load_review(request,object_id,model):
    try:
        try:model=model.split('_')[0]
        except:pass
        user=request.user
        try:review=MpttComment.objects.get(object_pk=object_id,user=user,content_type__model__iexact=model)
        except:review=None
        ctype=ContentType.objects.get(model__iexact=model)
        target=ctype.get_object_for_this_type(id=object_id)
        if not user.is_authenticated():user = None
        data = {'user':user,"object":target,'update':review}
        display_html=render_to_string('comments/review_form.html',data,context_instance=RequestContext(request))
        if review:
            review = review.id
        send_data={'display_html':display_html,'review':review,'status':'success'}
    except:
        send_data={'status':'fail'}
    return HttpResponse(simplejson.dumps(send_data))

def load_comment_form(request,object_id,model):
    try:
        try:model=model.split('_')[0]
        except:pass
        user=request.user
        ctype=ContentType.objects.get(model__iexact=model)
        target=ctype.get_object_for_this_type(id=object_id)
        if not user.is_authenticated():user = None
        data = {'user':user,"object":target}
        display_html=render_to_string('comments/form.html',data,context_instance=RequestContext(request))
        send_data={'display_html':display_html,'status':'success'}
    except:
        send_data={'status':'fail'}
    return HttpResponse(simplejson.dumps(send_data))

def like_dislike(request):
    try:
        comment_id = request.GET['cid']
        type = request.GET['type']
        comment = get_object_or_404(MpttComment, pk=comment_id)
        target = comment.content_object
    except:
        data = {'status':'error'}
        return HttpResponse(simplejson.dumps(data))
    if type=='1':
        repeat = 'n'
        try:
            if request.session['comment_like%s'%(comment.id)] != comment.id:
                try:
                    if request.session['comment_dislike%s'%(comment.id)] == comment.id:
                        del request.session['comment_dislike%s'%(comment.id)]
                        comment.dislike = comment.dislike - 1
                        repeat = comment.dislike
                except:pass        
                request.session['comment_like%s'%(comment.id)] = comment.id
                comment.like = comment.like + 1
                comment.save()
            else:
                data = {'status':'error'}
                return HttpResponse(simplejson.dumps(data))
        except:
            try:
                try:
                    if request.session['comment_dislike%s'%(comment.id)] == comment.id:
                        del request.session['comment_dislike%s'%(comment.id)]
                        comment.dislike = comment.dislike - 1
                        repeat = comment.dislike
                except:pass        
                request.session['comment_like%s'%(comment.id)] = comment.id
                comment.like = comment.like + 1
                comment.save()
            except:return HttpResponse('error')
        data = {'status':'working','repeat':repeat,'count':comment.like - comment.dislike, 'like_count':comment.like, 'dislike_count':comment.dislike}
        return HttpResponse(simplejson.dumps(data))
    else:
         repeat = 'n'
         try:
            if request.session['comment_dislike%s'%(comment.id)] != comment.id:
                try:
                    if request.session['comment_like%s'%(comment.id)] == comment.id:
                        del request.session['comment_like%s'%(comment.id)]
                        comment.like = comment.like - 1
                        repeat = comment.like
                except:pass        
                request.session['comment_dislike%s'%(comment.id)] = comment.id
                comment.dislike = comment.dislike + 1
                comment.save()
            else:
                data = {'status':'error'}
                return HttpResponse(simplejson.dumps(data))
         except:
            try:
                if request.session['comment_like%s'%(comment.id)] == comment.id:
                    del request.session['comment_like%s'%(comment.id)]
                    comment.like = comment.like - 1
                    repeat = comment.like
            except:pass        
            request.session['comment_dislike%s'%(comment.id)] = comment.id
            comment.dislike = comment.dislike + 1
            comment.save()
         data = {'status':'working','repeat':repeat,'count':comment.like - comment.dislike, 'like_count':comment.like, 'dislike_count':comment.dislike}
         return HttpResponse(simplejson.dumps(data))
                
def flag(request):
    try:
        comment_id = request.GET['cid']
        comment = get_object_or_404(MpttComment, pk=comment_id)
        target = comment.content_object
    except:return HttpResponse('0')
    try:
        if request.session['comment_flag%s'%(comment.id)] != comment.id:
            request.session['comment_flag%s'%(comment.id)] = comment.id
            comment.flag = comment.flag + 1
            comment.save()
        else:return HttpResponse('0')
    except:
        try:
            request.session['comment_flag%s'%(comment.id)] = comment.id
            comment.flag = comment.flag + 1
            comment.save()
        except:return HttpResponse('0')     
    return HttpResponse('1')
    
def confirmation_view(template, doc="Display a confirmation view."):
    """
    Confirmation view generator for the "comment was
    posted/flagged/deleted/approved" views.
    """
    def confirmed(request):
        comment = None
        if 'c' in request.GET:
            try:
                comment = MpttComment.objects.get(pk=request.GET['c'])
            except ObjectDoesNotExist:
                pass
        return render_to_response(template,{'comment': comment},context_instance=RequestContext(request))

    confirmed.__doc__ = textwrap.dedent("""\
        %s

        Templates: `%s``
        Context:
            comment
                The posted comment
        """ % (doc, template)
    )
    return confirmed

comment_done_ajax = confirmation_view(template = "comments/posted_ajax.html",doc = """Display a "comment was posted" success page.""")
comment_done = confirmation_view(template = "comments/posted.html",doc = """Display a "comment was posted" success page.""")

def comment_tree_json(request, object_list, tree_id, cutoff_level, bottom_level):

    if object_list:
        json_comments = {'end_level': object_list[-1].level, 'end_pk': object_list[-1].pk}

        template_list = [
            "comments/display_comments_tree.html",
        ]
        json_comments['html'] = render_to_string(
            template_list, {
                "comments" : object_list,
                "cutoff_level": cutoff_level,
                "bottom_level": bottom_level
            },
            RequestContext(request, {})
        )

        return json_comments
    return {}

def comments_more(request, from_comment_pk):

    offset = getattr(settings, 'MPTT_COMMENTS_OFFSET', 25)

    try:
        comment = MpttComment.objects.select_related('content_type').get(pk=from_comment_pk)
    except MpttComment.DoesNotExist:
        raise Http404

    cutoff_level = 3
    bottom_level = 0

    qs = MpttComment.objects.filter(
        tree_id=comment.tree_id,
        lft__gte=comment.lft+1,
        level__gte=1,
        level__lte=cutoff_level
    ).order_by('tree_id', 'lft').select_related('user')

    until_toplevel = []
    remaining = []
    toplevel_reached = False
    remaining_count = qs.count() - offset

    for comment in qs[:offset]:

        if comment.level == 1:
            toplevel_reached = True

        if toplevel_reached:
            remaining.append(comment)
        else:
            until_toplevel.append(comment)

    json_data = {'remaining_count': remaining_count, 'comments_for_update': [], 'comments_tree': {} }

    for comment in until_toplevel:
        json_comment = {'level': comment.level, 'pk': comment.pk}
        template_list = [
            "comments/display_comment.html",
        ]
        json_comment['html'] = render_to_string(
            template_list, {
                "comment" : comment,
                "cutoff_level": cutoff_level,
                "collapse_levels_above": 2
            },
            RequestContext(request, {})
        )
        json_data['comments_for_update'].append(json_comment)

    json_data['comments_tree'] = comment_tree_json(request, remaining, comment.tree_id, cutoff_level, bottom_level)

    return http.HttpResponse(simplejson.dumps(json_data), mimetype='application/json')

def comments_subtree(request, from_comment_pk, include_self=None, include_ancestors=None):

    try:
        comment = MpttComment.objects.select_related('content_type').get(pk=from_comment_pk)
    except MpttComment.DoesNotExist:
        raise Http404

    cutoff_level = comment.level + getattr(settings, 'MPTT_COMMENTS_CUTOFF', 3)
    bottom_level = not include_ancestors and (comment.level - (include_self and 1 or 0)) or 0

    related = getattr(settings, 'MPTT_COMMENTS_SELECT_RELATED', None)

    qs = MpttComment.objects.filter(
        tree_id=comment.tree_id,
        lft__gte=comment.lft + (not include_self and 1 or 0),
        lft__lte=comment.rght,
        level__lte=cutoff_level - (include_self and 1 or 0)
    ).order_by('tree_id', 'lft')

    if related:
        qs = qs.select_related(*related)
    
    is_ajax = request.GET.get('is_ajax') and '_ajax' or ''

    if is_ajax:

        json_data = {'comments_for_update': [], 'comments_tree': {} }
        json_data['comments_tree'] = comment_tree_json(request, list(qs), comment.tree_id, cutoff_level, bottom_level)

        return http.HttpResponse(simplejson.dumps(json_data), mimetype='application/json')

    else:

        target = comment.content_object
        model = target.__class__

        template_list = [
            "comments/%s_%s_subtree.html" % tuple(str(model._meta).split(".")),
            "comments/%s_subtree.html" % model._meta.app_label,
            "comments/subtree.html"
        ]

        comments = list(qs)
        if include_ancestors:
            comments = list(comment.get_ancestors())[1:] + comments

        return render_to_response(
            template_list, {
                "comments" : comments,
                "bottom_level": bottom_level,
                "cutoff_level": cutoff_level - 1,
                "collapse_levels_above": cutoff_level - (include_self and 2 or 1),
                "collapse_levels_below": comment.level

            },
            RequestContext(request, {})
        )
        
        
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

def get_initial_mptt_comment_list(request,object_id,model,appname):
    try:
        try:model=model.split('_')[0]
        except:pass
        user=request.user
        ctype=ContentType.objects.get(model__iexact=model)
        target=ctype.get_object_for_this_type(id=object_id)
        if not user.is_authenticated():user = None
        data = {"object":target,"appname":appname}
        data.update(get_all_comment_settings())
        return render_to_response('comments/ajax_initial_comments.html',data, context_instance=RequestContext(request))
    except:
        return render_to_response('default/article/displayarticles.html',data, context_instance=RequestContext(request))
    