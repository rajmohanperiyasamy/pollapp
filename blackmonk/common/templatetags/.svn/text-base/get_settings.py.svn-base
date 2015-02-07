from django.template import Library, Node
from django import template
 
from django.conf import settings
from common.utils import get_global_settings
     
register = Library()

def resolve_variable_or_literal(path, context):
    try:
        result = template.resolve_variable(path, context)
    except template.VariableDoesNotExist:
        if path.isdigit():
            result = int(path)
        else:
            result = path
    return result

class fa_function(Node):
    def __init__(self, f_str):
        self.f_str = f_str

    def render(self, context):
        s_key = str(resolve_variable_or_literal(self.f_str, context))
        
        global_settings = get_global_settings()
        a = 'global_settings.%s' % (s_key)
        return eval(a) 
            

@register.tag
def get_settings(parser, token):
    bits = token.contents.split()
    if len(bits) != 2:
        raise TemplateSyntaxError, "get_settings tag takes exactly one argument"
    return fa_function(bits[1])







#get_latest = register.tag(get_settings)
