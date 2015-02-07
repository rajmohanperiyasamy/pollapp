from common.models import SignupSettings
from django.template import Library,Node

register = Library()
signup_obj=SignupSettings.objects.all()

@register.tag
def load_signup_obj(parser, token):
    """
    {% load_signup_obj %}
    """
    return SignupSettingsClass()

class SignupSettingsClass(Node):
    def render(self, context):
        try:context['signup_settings'] = signup_obj[0]
        except:context['signup_settings']=None
        return ''


