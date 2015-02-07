from django.template import Library,Node,Variable
from django.contrib.contenttypes.models import ContentType

from common.models import CommentSettings,AvailableApps
from mptt_comments.models import MpttComment


register = Library()

@register.filter
def class_name(value):
    try:
        try:return value.__class__.__name__.split('_')[0]
        except:return value.__class__.__name__ 
    except:return '' 

@register.tag
def load_comment_config_obj(parser, token):
    """
    {% load_comment_config_obj %}
    """
    tag, app = token.split_contents()
    return CommentConfigClass(app)

class CommentConfigClass(Node):
    def __init__(self,app):
        self.app = Variable(app)
    def render(self, context):
        app = self.app.resolve(context)
        model=class_name(app).lower()
        try:model=model.split('_')[0]
        except:pass
        if model=='photoalbum':model='photos'
        elif model=='theatres':model='movies'
        elif model=='product':model='shop'
        elif model=='entry':model='community'
        elif model in ['article','attraction','event','community']:model=str(model)+'s'
        try:
            if model!='venue':
                apps=AvailableApps.objects.get(slug__iexact=model,status='A',comment='A')
            obj=CommentSettings.get_or_create_obj()
            context['cc_comment_enabled']=True
            context['cc_like_dislike'] = obj.like_dislike
            context['cc_flag'] = obj.flag
            context['cc_discuss_comment'] = obj.discuss_comment
            context['cc_discuss_shortcut'] = obj.discuss_shortcut
            context['cc_threaded'] = obj.threaded
            context['cc_avatar'] = obj.avatar
            context['cc_rating'] = obj.rating
            context['cc_approval']=obj.approval
        except:
            context['cc_comment_enabled']=False
        return ''
    
@register.tag
def load_comment_config_obj_staff(parser, token):
    """
    {% load_comment_config_obj %}
    """
    return CommentCongifClassStaff()

class CommentCongifClassStaff(Node):
    def render(self, context):
        try:
            apps=AvailableApps.objects.filter(status='A',comment='A').exclude(comment='N').order_by('slug')
            applist=[]
            for app in apps:
                statt_applist={}
                try:
                    if app.slug in ['articles','attractions','events']:statt_applist['slug']=app.slug[:-1]
                    else:statt_applist['slug']=app.slug
                except:pass
                statt_applist['name']=app.name
                applist.append(statt_applist)
            context['statt_applist']=applist
        except:pass
        return ''

        
