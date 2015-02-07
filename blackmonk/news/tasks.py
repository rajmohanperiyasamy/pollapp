import celery
import datetime
from time import strptime

from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from django.utils.html import strip_tags
from django.db.models import Q

from common import feedparser
from common.utils import date_fun,get_global_settings
from common.getunique import getUniqueValue,getSlugData
from news.models import News,Provider,Category
 
@celery.task(name='tasks.news_feed')
def news_feed():
    User = get_user_model()
    try:user = User.objects.get(id=1)
    except:user = User.objects.filter(is_superuser=True)[:1][0]
    
    for data in Category.objects.all():
        for provider in Provider.objects.filter(is_active=True):
            url='http://news.google.com/news?pz=1&cf=all&ned=in&hl=en&q='+get_global_settings().city+'+'+data.name+'+'+provider.address+'&cf=all&output=rss'
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = (entry.title).split(' - ')[0]
                pub_date = entry.date[5:22]
                published = datetime.datetime.strptime(pub_date, "%d %b %Y %H:%M")
                
                try:News.objects.get(Q(url=(entry.id).split('cluster=')[1]) | Q(title=title))
                except News.DoesNotExist:
                    if date_fun()['cmp_date']<=published:
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
                except:pass
    return 'Success'



