import getsettings

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
User = get_user_model()

from movies.models import Movies
from community.models import Entry
from polls.models import Poll


def fix_permission():
    advice=ContentType.objects.get_for_model(Entry)
    movies=ContentType.objects.get_for_model(Movies)
    polls=ContentType.objects.get_for_model(Poll)
    
    try:a_permission=Permission.objects.get(content_type=advice,codename='publish_advice')
    except:
        a_permission=Permission(name='Can Publish Advice',content_type=advice,codename='publish_advice')
        a_permission.save()
    try:m_permission=Permission.objects.get(content_type=movies,codename='publish_movies')
    except:
        m_permission=Permission(name='Can Publish Movies',content_type=movies,codename='publish_movies')
        m_permission.save()
    try:p_permission=Permission.objects.get(content_type=polls,codename='publish_polls')
    except:
        p_permission=Permission(name='Can Publish Polls',content_type=polls,codename='publish_polls')
        p_permission.save()
    
fix_permission()