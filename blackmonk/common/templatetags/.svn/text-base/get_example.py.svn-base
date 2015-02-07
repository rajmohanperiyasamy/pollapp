from django.template import Library, Node
from django import template

from django.conf import settings

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

class fa_example(Node):
    def __init__(self, f_str):
        self.f_str = f_str

    def render(self, context):
        s_key = str(resolve_variable_or_literal(self.f_str, context))
        
        from common.templatetags import example
        a = 'example.%s' % s_key
        return eval(a) 

@register.tag
def example(parser, token):
    key1 = token.contents.split()
    return fa_example(key1[1])