import celery
import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings as my_settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags
from django.utils.importlib import import_module
import time

from common import feedparser
from common.getunique import getUniqueValue, getSlugData
from common.utils import custom_cache, get_global_settings
from haystack.management.commands import update_index, clear_index
from news.models import News, Provider, Category


SELECT_WINNER_ONLY_FOR_PUBLISHED_ITEMS = True
User = get_user_model()

@custom_cache(600)
def date_fun():
    today=datetime.date.today()
    return {
            'today':today,
            "three_days_after":today + relativedelta(days= +3),
            "thirthy_days_before": today + relativedelta(days= -30),
            "cmp_date": datetime.datetime.now() - datetime.timedelta(3)
            }

@celery.task(name='tasks.celery_rebuild_index')
def celery_rebuild_index():
    celery.current_task.update_state(state="PROGRESS")
    clear_index.Command().handle(yes_or_no='y')
    time.sleep(10)
    update_index.Command().handle()
    return "Success"

@celery.task(name='tasks.news_feed')
def news_feed():
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
           

@celery.task(name='tasks.clear_session')
def clear_session():
    engine = import_module(my_settings.SESSION_ENGINE)
    SessionStore = engine.SessionStore

    expired_sessions = Session.objects.filter(expire_date__lte=datetime.datetime.now())

    for session in expired_sessions:
        store = SessionStore(session.session_key)
        store.delete()
