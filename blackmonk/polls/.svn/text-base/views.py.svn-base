from datetime import date
import datetime

from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from common.models import ModuleNames
from common.views import get_poll_details
from polls.models import Poll,Choices

def ajax_poll_voting(request,template='default/polls/ajax-poll-results.html'):
    today = datetime.date.today()
    today_time = datetime.datetime.today()
    type = request.GET['mode']
    poll = Poll.objects.get(id=request.GET['pid'])
    choice = Choices.objects.filter(poll = poll).order_by('id')
    try:
        request.session['poll%s'%(poll.id)]
        status='notvoted'
    except:
        request.session['poll%s'%(poll.id)] = poll.id
        if type == 'single':
            vote = request.GET['vote']
        elif type == 'multi':
            vote = request.GET['vote']
        for c in choice:
            if type == 'single':
                if vote == c.choice:
                    c.vote = int(c.vote)+1
                    c.save()
            elif type =='multi': 
                new_vote = vote.split('>>')
                vote_len = len(new_vote)
                i=0
                for v in new_vote:
                    if (i == vote_len):
                        new_vote[i].replace('>>')
                        i = i+1
                 
                for v in new_vote:
                    if v == c.choice:
                        c.vote = int(c.vote)+1
                        c.save()
        status='voted'
                       
    
    show_choice = True
    no_msg = False
    try:
        if request.session['poll%s'%(poll.id)] == poll.id:
           show_choice = False
    except:pass
    if status=='voted':
        voted = True
    elif status=='notvoted':
        voted = False    
        no_msg=True
    try:
        view = request.GET['result']
    except:pass    
    total_votes = 0
    
    for c in choice:
        total_votes = total_votes + int(c.vote)
    
    perc=[]
    for c in choice:
        vote_prcnt=(int(c.vote)*1.0/int(total_votes))*100
        perc.append(int(vote_prcnt))
    
    results = []
    i = 0
    for c in choice:
        results.append({'choice': c.choice, 'votes':c.vote, 'perc':perc[i] })
        i += 1
    return render_to_response(template,locals(), context_instance=RequestContext(request)) 

def ajax_view(request):
    template='default/polls/ajax-poll-view.html'
    if request.GET['view'] == 'result':template='default/polls/ajax-poll-results.html'
    view = request.GET['view']
    try:
        id      = request.GET['pid']
        poll    = Poll.objects.get(id=id)
        choice  = Choices.objects.filter(poll = poll).order_by('id')
        total_votes = 0
        for c in choice:
            total_votes = total_votes + int(c.vote)
                    
        perc=[]
        for c in choice:
            vote_prcnt=(int(c.vote)*1.0/int(total_votes))*100
            perc.append(int(vote_prcnt))
       
        results = []
        i = 0
        for c in choice:
            results.append({'choice': c.choice, 'votes':c.vote, 'perc':perc[i] })
            i += 1
    except:pass
    return render_to_response(template,locals(), context_instance=RequestContext(request))

def poll_home(request,template='default/polls/home.html'):
    data={}
    polldata=get_poll_details(request)
    data.update(polldata)
    data['seo'] = ModuleNames.get_module_seo(name='polls')
    data['polls']=Poll.objects.filter(status='E')
    return render_to_response(template,data, context_instance=RequestContext(request))

def ajax_load_poll_data(request,template='default/polls/ajax_load_poll_data.html'):
    data={}
    send_data={}
    try:
        polldata = get_poll_details(request)
        html=render_to_string(template,polldata,context_instance = RequestContext(request))
        send_data['html'] = html
        send_data['status'] = 1
        return HttpResponse(simplejson.dumps(send_data))
    except:
        send_data['status'] = 0
        return HttpResponse(simplejson.dumps(send_data))


