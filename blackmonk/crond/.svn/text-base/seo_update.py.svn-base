import getsettings

from article.models import ArticleCategory
from classifieds.models import ClassifiedCategory
from attraction.models import AttractionCategory

from business.models import BusinessCategory
from bookmarks.models import BookmarkCategory
from gallery.models import PhotoCategory
from events.models import EventCategory
from videos.models import VideoCategory
from common.models import ModuleNames
from common.utils import ds_pagination,get_global_settings

global_settings = get_global_settings()
city = global_settings.city

replace_word = 'Moscow.me'

words_dic={'Onlineclalgary.com':replace_word,'Onlineclalgary.net':replace_word,
           'onlineclalgary.net':replace_word,'LocalEngine':replace_word,
           'demo.blackmonk.com':replace_word,'demo.Blackmonk.com':replace_word,'calgary':city,'Calgary':city}


def __update_seo_content(obj,i,j):
    obj.seo_title = obj.seo_title.replace(i,j)
    obj.seo_description = obj.seo_description.replace(i,j)
    obj.save()
    

categories = BusinessCategory.objects.all()
for cat in categories:
    for i,j in words_dic.iteritems():
        try:
            __update_seo_content(cat,i,j)
        except:
            pass

categories = BookmarkCategory.objects.all()
for cat in categories:
    for i,j in words_dic.iteritems():
        try:
            __update_seo_content(cat,i,j)
        except:
            pass
        
categories = ArticleCategory.objects.all()
for cat in categories:
    for i,j in words_dic.iteritems():
        try:
            __update_seo_content(cat,i,j)
        except:
            pass
        
categories = PhotoCategory.objects.all()
for cat in categories:
    for i,j in words_dic.iteritems():
        try:
            __update_seo_content(cat,i,j)
        except:
            pass
        
categories = EventCategory.objects.all()
for cat in categories:
    for i,j in words_dic.iteritems():
        try:
            __update_seo_content(cat,i,j)
        except:
            pass
        
categories = VideoCategory.objects.all()
for cat in categories:
    for i,j in words_dic.iteritems():
        try:
            __update_seo_content(cat,i,j)
        except:
            pass
        
categories = ModuleNames.objects.all()
for cat in categories:
    for i,j in words_dic.iteritems():
        try:
            __update_seo_content(cat,i,j)
        except:
            pass
        
        
        
        
