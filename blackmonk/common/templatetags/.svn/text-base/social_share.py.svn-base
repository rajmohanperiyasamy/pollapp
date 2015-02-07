from common.models import SocialSettings,SignupSettings
from django.template import Library,Node

register = Library()

@register.tag
def load_socialshare_obj(parser, token):
    """
    {% load_socialshare_obj %}
    """
    return SocialShareSettingsClass()

class SocialShareSettingsClass(Node):
    def render(self, context):
        social_obj=SocialSettings.get_or_create_obj()
        context['social'] = social_obj
        return ''
    
@register.tag
def load_signin_obj(parser, token):
    """
    {% load_signin_obj %}
    """
    return SignupSettingsClass()

class SignupSettingsClass(Node):
    def render(self, context):
        social_obj=SignupSettings.get_or_create_obj()
        context['signup'] = social_obj
        return ''