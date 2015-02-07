
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from common.models import ModuleNames
from meetup.utils import get_meetups,get_all_meetups,get_more_meetups

Meetup_Categories = [{'name': 'Adventurers', 'slug': u'adventurers'}, {'name': 'Art', 'slug': u'art'}, {'name': 'Business Networking', 'slug': u'business-networking'},
 {'name': 'Business Strategy and Networking', 'slug': u'businessnetwork'}, {'name': 'Dating and Relationships', 'slug': u'dating-and-relationships'},
 {'name': 'Entrepreneur', 'slug': u'entrepreneur'}, {'name': 'Exercise and Fun', 'slug': u'exercise-and-fun'}, {'name': 'Fitness', 'slug': u'fitness'},
 {'name': 'Food Lovers', 'slug': u'food-lovers'}, {'name': 'Friends', 'slug': u'friends'}, {'name': 'Fun Times', 'slug': u'fun-times'}, {'name': 'Happy Hours', 'slug': u'happy-hours'},
 {'name': 'Health and Wellness', 'slug': u'health-and-wellness'}, {'name': 'Hiking', 'slug': u'hiking'}, {'name': 'Live Music', 'slug': u'livemusic'},
 {'name': 'Make New Friends', 'slug': u'make-new-friends'}, {'name': 'Meeting New People', 'slug': u'meeting-new-people'}, {'name': 'Movie Fans', 'slug': u'movies'},
 {'name': 'Music', 'slug': u'music'}, {'name': 'New In Town', 'slug': u'newintown'}, {'name': 'Night Life', 'slug': u'night-life'}, {'name': 'Outdoors', 'slug': u'outdoors'},
 {'name': 'Photography', 'slug': u'photo'}, {'name': 'Real Estate Buying & Investing', 'slug': u'realestate'}, {'name': 'Singles', 'slug': u'singles'},
 {'name': 'Small Business', 'slug': u'smallbiz'}, {'name': 'Social', 'slug': u'social'}, {'name': 'Software Developers', 'slug': u'softwaredev'},
 {'name': 'Spirituality', 'slug': u'spirituality'}, {'name': 'Sports & Recreation', 'slug': u'sports'}, {'name': 'Travel', 'slug': u'travel'},
 {'name': 'Web Technology', 'slug': u'web'}, {'name': 'Wellness', 'slug': u'wellness'}, {'name': "Women's Social", 'slug': u'women'}]


def meetups(request):
    meetups = get_meetups()
    data = {'meetups':meetups}
    return render_to_response('default/meetup/part-meetup-list.html', data)

#@cache_page(60 * 5)
def index(request, category=None, template='default/meetup/index.html'):
    from django.template.defaultfilters import slugify
    data = {}
    cache.clear()
    if  category:
        if cache.get(category):
            meetups,more_meet = cache.get(category),cache.get(category+'more')
        else:
            meetups,more_meet = get_all_meetups(category)
            cache.set(category,meetups,60*30)
            cache.set(category+'more',more_meet,60*30)
    else:
        if cache.get("allmeetups"):
            meetups,more_meet = cache.get("allmeetups"),cache.get('allmore')
        else:
            meetups,more_meet = get_all_meetups()
            cache.set('allmetups',meetups,60*30)
            cache.set('allmore',more_meet,60*30)
    data['meetups'] = meetups
    data['more_meet'] = more_meet
    data['categories'] = Meetup_Categories
    data['selected_category'] = category
    data['seo'] = ModuleNames.get_module_seo(name='meetup')
    return render_to_response(template, data, context_instance=RequestContext(request))

def more_meetups(request, template='default/meetup/part-meetup-list.html'):
    send_data = {}
    try:
        category = request.GET.get('category',None)
        more_meetups_url = request.GET['more_meetups']
        meetups,more_meet = get_more_meetups(more_meetups_url,category)
        data = {'meetups':meetups, 'more_meet':more_meet, 'selected_category':category}
        send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
        if meetups:
            mtp_list= True
        else:
            mtp_list = False
        send_data['mtp_list'] = mtp_list    
        send_data['status'] = True   
    except:
        send_data['status'] = False  
    return HttpResponse(simplejson.dumps(send_data))