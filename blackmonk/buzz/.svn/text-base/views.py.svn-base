from urllib import urlencode
import datetime,time

from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from django.utils import simplejson
from django.utils.translation import ugettext as _


from common.models import ModuleNames
from buzz.models import TwitterAPISettings,BuzzTwitterLists,BuzzTwitterKeywords,Category
from buzz.twitter import *

from common.oauthtwitter import *

tweets_per_page = 20

def get_oauth_api():
    import twitter_oauth
    try:
        api_settings = TwitterAPISettings.objects.all()[:1][0]
    except:
        raise Http404
    
    OT = api_settings.twitter_auth_key
    OTS = api_settings.twitter_auth_secret
    CK = api_settings.twitter_consumer_key
    CKS = api_settings.twitter_consumer_secret
    oa_api = twitter_oauth.Api(CK, CKS,OT, OTS)
    return oa_api



def buzz_home(request,template='default/buzz/buzz_home.html'):
    categories_obj = Category.objects.filter(occupied=True).order_by('name')
    api = get_oauth_api()
    data={}
    q = False
    try:
        q = request.GET['q']
        q1 = q.replace(' ', '+').replace('#','%23')
        keyword_url = "&q="+q1
        data['q'] = q
        data['q_url'] = q1
    except:
        #Build keyword url
        keyword_obj = BuzzTwitterKeywords.objects.all()
        loop =  keyword_obj.count()
        if loop == 0:
            keyword_url = ""
        else:
            keyword_url = "&q="
            for i in range(loop):
                if keyword_url == "&q=":
                    keyword_url = keyword_url + str(keyword_obj[i].keyword)
                else:
                    keyword_url=keyword_url+"+OR+"+str(keyword_obj[i].keyword)
    #take the number of tweets per page
    
    per_page = str(tweets_per_page)
    
    next_page = "2"
    page = "1"
    
    page_url = "&rpp="+per_page+"&page="+page
    data['categories_dir'] = categories_obj
    data['next_page'] = next_page
    data['page'] = page
    data['load_home_page'] = True
    data['buzz_nav'] = 'home'
    #Trends
    try:data['trends'] = getTrends()
    except:data['trends'] = None
   
    try:
        data['tweets'] =  api.get_friends_timeline(None,None,None,per_page,page)
        data['tweets_home_twitter'] = True
    except:data['tweets'] = None
    #Hiding the more button if the number of tweets is less then the page per tweets
    if data['tweets']:
        count = 0
        for i in data['tweets']:
            count += 1
        data['hide_more'] = 'show'
        
        if count < int(per_page):
            data['hide_more'] = 'hide'
    data['seo'] = ModuleNames.get_module_seo(name='buzz')
    return render_to_response(template,data, context_instance=RequestContext(request))

def retrieve_buzz(request,category=False):
    categories_obj = Category.objects.filter(occupied=True).order_by('name')
    
    api = getOAuthApi()

    try:cat_nav_obj = Category.objects.get(slug=category)
    except:return HttpResponseRedirect('/buzz/')
    
    buzz_nav = cat_nav_obj.name
    
    lists_obj = BuzzTwitterLists.objects.get(category__id = cat_nav_obj.id)
    lists = lists_obj.lists_name
    
    per_page = str(tweets_per_page)
    
    data={}
    next_page = "2"
    page = "1"
    per_page_url = "&per_page="+per_page
    
    #seo
    seo_obj = Category.objects.get(id = cat_nav_obj.id)
    if seo_obj.seo_title != None:
        data['seo_title'] = seo_obj.seo_title
    else:
        data['seo_title'] = ''
    if seo_obj.seo_description != None:
        data['seo_description'] = seo_obj.seo_description
    else:
        data['seo_description'] = ''
    
    #Trends
    try:data['trends'] = getTrends()
    except:data['trends'] = None
    
    data['categories_dir'] = categories_obj
    data['category'] = category
    data['next_page'] = next_page
    data['buzz_nav'] = buzz_nav

    try:data['tweets'] = api.GetListTweets(lists,page,per_page_url)
    except:data['tweets'] = None

    if data['tweets']:
        count = 0
        for i in data['tweets']:
            count += 1
        data['hide_more'] = 'show'
        if count < int(per_page):
            data['hide_more'] = 'hide'
    
    return render_to_response('default/buzz/buzz_home.html',data, context_instance=RequestContext(request))


def ajax_retrieve_buzz(request,category=False):
    api = get_oauth_api()
    try:cat_obj = Category.objects.get(slug=category)
    except:return HttpResponse('empty')
        
    lists_obj = BuzzTwitterLists.objects.get(category__id = cat_obj.id)
    lists = lists_obj.lists_name
   
    per_page = str(tweets_per_page)
    try:
        page  = int(request.GET['page'])
        page  = str(page)
    except: page = "1"
    
    data = {}
    per_page_url = "&per_page="+per_page 
    
    try:
        data['tweets'] = api.GetListTweets(lists,page,per_page_url)
        data['tweets_from_backup'] = 'no'
    except:data['tweets'] = None
    
    if data['tweets'] == []: return HttpResponse('empty')
    else:
        return render_to_response('default/buzz/ajax_buzz_retrieve_tweets.html',data, context_instance=RequestContext(request))
    
def ajax_retrieve_search(request):
    api = get_oauth_api()
    data = {}
    per_page = str(tweets_per_page)
    q = False
    try:
        q = request.GET['q']
        q1 = q.replace(' ', '+').replace('#','%23')
        keyword_url = "&q="+q1
        data['q'] = q
    except:
        #Build keyword url
        keyword_obj = BuzzTwitterKeywords.objects.all()
        loop =  keyword_obj.count()
        if loop == 0:
            keyword_url = ""
        else:
            keyword_url = "&q="
            for i in range(loop):
                if keyword_url == "&q=":
                    keyword_url = keyword_url + str(keyword_obj[i].keyword)
                else:
                    keyword_url=keyword_url+"+OR+"+str(keyword_obj[i].keyword)
    
    try:page  = request.GET['page']
    except:page = "1"
        
    page_url = "&rpp="+per_page+"&page="+page
    
    try:
        data['tweets'] = api.get_friends_timeline(None,None,None,per_page,page)
        data['tweets_from_backup'] = 'no'
    except:data['tweets'] = None
           
    if data['tweets'] == []:return HttpResponse('empty')
    else:
        return render_to_response('default/buzz/ajax_buzz_search_tweets.html',data, context_instance=RequestContext(request))


def getOAuthApi():
    api_settings = TwitterAPISettings.objects.all()[:1][0]
    api = OAuthApi(consumer_key=api_settings.twitter_consumer_key, consumer_secret=api_settings.twitter_consumer_secret, token=api_settings.twitter_auth_key, token_secret=api_settings.twitter_auth_secret)
    return api
