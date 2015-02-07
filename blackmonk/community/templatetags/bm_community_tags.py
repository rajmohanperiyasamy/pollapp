from django.template import Library
from community.models import Entry
register = Library()

@register.filter
def get_session_like(eid, request):
    try:
        if request.session['like%s'%(eid)] == eid:
            return True
        else:
            return False
    except:
        return False
    
@register.filter
def get_session_dislike(eid, request):
    try:
        if request.session['dislike%s'%(eid)] == eid:
            return True
        else:
            return False
    except:
        return False