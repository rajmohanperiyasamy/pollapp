from django.template import Library, Node
from django import template
     
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
        #f_str = context['nx'].logo
        f_str = resolve_variable_or_literal(self.f_str, context)
        #context['latest_links'] = '[{fazal sulaiman}]'
        a=str(f_str).split('/')
        try:
            return a[len(a)-1]
        except:
            return a[0]


def get_filename(parser, token):
    """
    eg:
        {% get_filename images/test/demo.jpg %}
        {% get_filename module.image %}
    """
    bits = token.contents.split()
    if len(bits) != 2:
        raise TemplateSyntaxError, "get_latest_links tag takes exactly one argument"
    return fa_function(bits[1])

    
get_latest = register.tag(get_filename)
