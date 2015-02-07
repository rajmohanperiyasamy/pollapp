#! /home/blackmonk/virtualenvs/bm/bin/python

import datetime,time
from time import strptime
from datetime import timedelta
import getsettings
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.html import strip_tags
from django.db import models
from domains import *
from news.models import News,Provider,Category
from common.getunique import getUniqueValue,getSlugData
from common import feedparser
from common.utils import get_global_settings
from django.db import connection
from django.db.models import Q

cmp_date = datetime.datetime.now()-timedelta(3)


def get_keyword(globalsettings,data):
    step1 = data.split(' ')
    result = globalsettings.city+' news, social bookmarks, '+globalsettings.city+' information, '
    for val in step1:
        if len(val)>3:result = result + val + ', '
    return result

def __fetch_details(user,globalsettings):
    for data in Category.objects.all():
        for provider in Provider.objects.all():
            url='http://news.google.com/news?pz=1&cf=all&ned=in&hl=en&q='+globalsettings.city+'+'+data.name+'+'+provider.address+'&cf=all&output=rss'
            
            print url
            
            
            feed = feedparser.parse(url)
            print feed.entries
            for entry in feed.entries:
                title = (entry.title).split(' - ')[0]
                pub_date = entry.date[5:22]
                published = datetime.datetime.strptime(pub_date, "%d %b %Y %H:%M")
                
                #print "++++++++++++cmp_date,publisheddate"
                #print cmp_date
                #print published
                #print "++++++++++++cmp_date,publisheddate"
                
                try:News.objects.get(Q(url=(entry.id).split('cluster=')[1]) | Q(title=title))
                except News.DoesNotExist:
                    if cmp_date<=published:
                        news = News(created_on=published,modified_on=published,created_by=user,modified_by=user,is_active=True,is_feed=True)
                        news.title = title
                        try:news.provider = Provider.objects.get(address__icontains=((entry.id).split('cluster=')[1]).split('/')[2],is_active=True)
                        except:continue
                        news.seo_title = title[:90]
                        news.category =data
                        summary = ((entry.description).split('<font size="-1">'))[2]
                        news.summary = strip_tags((summary.split('</font>'))[0])
                        news.seo_description = news.summary[:175]
                        news.url = (entry.id).split('cluster=')[1]
                        news.status = 'P' 
                        news.slug = getUniqueValue(News,slugify(getSlugData(news.title)))
                        news.save()
                    else:continue
                except:
                    import sys
                    print "Errors",sys.exc_info()
                    pass

globalsettings=get_global_settings()
try:user = User.objects.get(id=1)
except:user = User.objects.filter(is_superuser=True)[:1][0]
__fetch_details(user,globalsettings)

