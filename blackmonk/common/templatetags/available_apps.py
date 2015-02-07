from common.models import AvailableApps
from django.template import Library,Node

register = Library()

@register.tag
def load_availableapps_obj(parser, token):
    """
    {% load_availableapps_obj %}
    """
    return AvailableAppClass()

class AvailableAppClass(Node):
    def render(self, context):
        availableapps_obj=AvailableApps.objects.filter(status='A')
        for aa in availableapps_obj:
            if aa.slug=="places-to-see":
                try:context['aa_things_to_do'] = aa
                except:context['aa_things_to_do']=None
            else:
                try:context['aa_'+aa.slug] = aa
                except:context['aa_'+aa.slug]=None
        return ''
    

@register.tag
def load_availableapp_obj(parser, token):
    """
    {% load_availableapp_obj %}
    """
    return AvailableAppsClass()

class AvailableAppsClass(Node):
    def render(self, context):
        availableapps_objs=AvailableApps.objects.filter(status='A').exclude(slug__in=['newsletter','usermgmt']).order_by('name')
        context['availableapps_objs'] = availableapps_objs
        return ''