from datetime import date
import datetime
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from time import strptime

from business.models import Business
from channels.models import Channel
from events.models import Event


def channels_home(request,channel_slug):
    try:
        channel = Channel.objects.get(slug=channel_slug, status = 'P')
        template = channel.template_name
        data = {'channel':channel}
    except:
        raise Http404
    return render_to_response(template, data, context_instance=RequestContext(request))


def latest_business_ajax(request,channel_slug):
    data={}
    channel = Channel.objects.get(slug=channel_slug, status = 'P')
    try:
        ch_id=request.GET['id']
        category_biz = Business.objects.filter(status='P',categories__id=ch_id).only('name','logo','slug','ratings').prefetch_related('categories','address').select_related('logo').order_by('-id').distinct()[:6]
    except:
        category_biz = Business.objects.filter(status='P',categories__in=channel.businesswidget.categories.all()).only('name','logo','slug','ratings').prefetch_related('categories','address').select_related('logo').order_by('-id').distinct()[:6]
    data['biz_html'] = render_to_string('default/channels/category_business_ajax.html',{'category_biz': category_biz},context_instance=RequestContext(request))
    return HttpResponse(simplejson.dumps(data))

def ajax_get_channel_events_by_date(request,channel_slug,template='default/events/ajax_events.html'):
    ''' channel page ajax method for retreiving events by date '''
    data={}
    send_data = {}
    channel = Channel.objects.get(slug=channel_slug, status = 'P')
    try:
        try:
            selected_date = datetime.datetime(*strptime(request.GET['sel_date'], "%Y-%m-%d")[0:3])
        except:
            selected_date = date.today()
        data['events'] = Event.objects.filter(start_date__lte=selected_date,end_date__gte=selected_date,status='P',category__in=channel.eventwidget.categories.all()).only("title","venue","slug","start_date","end_date","start_time","end_time").prefetch_related('category').order_by('-id').distinct()[:3]
        send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
        send_data['status'] = True
    except:send_data['status'] = False
    return HttpResponse(simplejson.dumps(send_data))