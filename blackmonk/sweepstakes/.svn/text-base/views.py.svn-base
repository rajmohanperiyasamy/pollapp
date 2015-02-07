from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.conf import settings as my_settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from common.models import ModuleNames,CommentSettings,Pages
from common.utils import get_global_settings
from usermgmt.newsletter import ajax_subscripe_newsletter
from sweepstakes.models import Sweepstakes,SweepstakesOffers,SweepstakesImages,SweepstakesPoints
from sweepstakes.models import SweepstakesQandA,SweepstakesParticipant
from sweepstakes.forms import SweepstakesParticipantForm
from sweepstakes.utils import LABLE_DIST_P,EXTRA_LABLE_DIST_P,LABLE_DIST,EXTRA_LABLE_DIST

def home(request,template='default/sweepstakes/home.html'):
    sweepstakes = Sweepstakes.objects.filter(status='P').order_by('-created_on')
    data ={'sweepstakes':sweepstakes}
    data['qandas']=SweepstakesQandA.objects.all().order_by("position")
    data['seo'] = ModuleNames.get_module_seo(name='sweepstakes')
    data['comment_settings']=CommentSettings.get_or_create_obj()
    return render_to_response(template,data, context_instance=RequestContext(request))

def detail(request,id,slug,template='default/sweepstakes/details.html'):
    try:sweepstakes = Sweepstakes.objects.get(id=id,slug=slug,status='P')
    except:raise Http404
    data ={'sweepstakes':sweepstakes}
    data['qandas']=SweepstakesQandA.objects.all()
    data['comment_settings']=CommentSettings.get_or_create_obj()
    available_apps=[]
    availableapps_points=SweepstakesPoints.objects.select_related('app','sweepstake').filter(sweepstake=sweepstakes)
    try:data['c_user']=c_user=SweepstakesParticipant.objects.get(sweepstakes=sweepstakes,participant=request.user)
    except:c_user=False
    for app in availableapps_points:
        d={'label':LABLE_DIST[app.app.slug],'text':LABLE_DIST_P[app.app.slug],'point':app.app_point}
        if app.app.slug in ['polls','deals']:d['url']='/'+str(app.app.slug)
        else:d['url']='/user/'+str(app.app.slug)
        if c_user:
            if app.app.slug in ['articles','attractions','events']:d['u_point']=app.get_points(request.user,app.app.slug[:-1])
            elif app.app.slug=='photos':d['u_point']=app.get_points(request.user,'photoalbum')
            else:d['u_point']=app.get_points(request.user,app.app.slug)

        available_apps.append(d)
        if app.app.slug in EXTRA_LABLE_DIST_P.keys():
            if app.app.slug=='advice':d={'label':EXTRA_LABLE_DIST[app.app.slug],'text':EXTRA_LABLE_DIST_P[app.app.slug],'point':sweepstakes.advice_e}
            elif app.app.slug=='discussions':d={'label':EXTRA_LABLE_DIST[app.app.slug],'text':EXTRA_LABLE_DIST_P[app.app.slug],'point':sweepstakes.discussions_e}
            d['url']='/'+str(app.app.slug)
            available_apps.append(d)
    data['available_apps']=available_apps
    return render_to_response(template,data, context_instance=RequestContext(request))

def register_user(request,id):
    if request.user.is_authenticated():
        sweepstakes=Sweepstakes.objects.get(id=id,status='P')
        data={'sweepstakes':sweepstakes}
        form=SweepstakesParticipantForm(user=request.user)
        try:
            user=SweepstakesParticipant.objects.get(sweepstakes__id=id,participant=request.user,status='A')
            data['user_msg']="You are already registered for this contest."  
            data['uc_exist']=True
            data['form']=form
            return render_to_response('default/sweepstakes/contest.html',data,RequestContext(request))
        except:
            user=SweepstakesParticipant.objects.filter(participant=request.user,status='A')
            if user:
                data['user_msg']="You are already registered for another active contest.If you continue other contest will be inactive.More see in FAQ"  
                c_exist=True
            else:c_exist=False
        data['c_exist']=c_exist
        if request.method=='POST':
            form = SweepstakesParticipantForm(request.POST)
            if form.is_valid():
                user.update(status='I')
                cform=form.save(commit=False)
                cform.sweepstakes=sweepstakes
                cform.participant=request.user
                cform.status='A'
                cform.reg_point=sweepstakes.reg_point
                cform.total=sweepstakes.reg_point
                cform.save()
                try:ajax_subscripe_newsletter(request.user.first_name,request.user.email,'html')
                except:pass
                sdata={'status':1,'points':sweepstakes.reg_point}
                return HttpResponse(simplejson.dumps(sdata))
            else:
                data['form']=form
                data['c_exist']=False
                return render_to_response('default/sweepstakes/contest.html',data,RequestContext(request))
        else:
            data['form']=form
            return render_to_response('default/sweepstakes/contest.html',data,RequestContext(request))
    else:return HttpResponseRedirect(reverse('ajax_signin')+"?type=contest")

def contest_rules(request,id):
    page=Pages.objects.get(id=id)
    return render_to_response('default/sweepstakes/rules.html',{'content':page.content})

def ajax_add_fbpoint(request,id):
    try:
        user=SweepstakesParticipant.objects.get(sweepstakes__id=id,participant=request.user,status='A')
        if not user.fb_point:
            user.fb_point=5
            user.total=user.total+user.fb_point
            user.save()
            sdata={'status':1,'points':user.fb_point,'tpoints':user.total}
        else:sdata={'status':2}
    except:sdata={'status':0}  
    return HttpResponse(simplejson.dumps(sdata))

def ajaxtellafriend(request,id):
    if request.method == 'POST':
        contest = Sweepstakes.objects.get(id=id)
        global_settings=get_global_settings()
        
        from_name = request.POST['from_name']
        to_name = request.POST['to_name']
        to_email = request.POST['to_email']
        msg = request.POST['msg']
        subject = from_name+' sent you the details for "'+contest.title+'" on '+global_settings.domain
        
        tell_a_friend_data = {}
        tell_a_friend_data['from_name'] = from_name
        tell_a_friend_data['to_name'] = to_name
        tell_a_friend_data['to_email'] = to_email
        tell_a_friend_data['subject'] = subject
        tell_a_friend_data['msg'] = msg
        tell_a_friend_data['contest'] = contest
        
        email_message = render_to_string("default/sweepstakes/invitefriendmail.html",tell_a_friend_data)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,[to_email])
        email.content_subtype = "html"
        
        if(email.send()):
            sdata={'success':1}
            try:
                user=SweepstakesParticipant.objects.get(sweepstakes__id=id,participant=request.user,status='A')
                if not user.friend_point:
                    user.friend_point=2
                    user.total+=user.friend_point
                    user.save()
                sdata={'success':1,'points':user.friend_point,'tpoints':user.total}
            except:
                pass
            return HttpResponse(simplejson.dumps(sdata))
        else:return HttpResponse(simplejson.dumps({'success':0}))
    return HttpResponse(simplejson.dumps({'success':0}))
