from common.models import AvailableModules,Pages
from django import template
from django.core.cache import cache

register = template.Library()

def build_menu(parser, token):
    """
    {% menu menu_name %}
    """
    try:
        tag_name, menu_name = token.split_contents()
    except:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
    return MenuObject(menu_name)

class MenuObject(template.Node):
    def __init__(self, menu_name):
        self.menu_name = menu_name

    def render(self, context):
        #current_path = context['request'].path
        #user = context['request'].user
        context['menuitems'] = get_items(self.menu_name)
        return ''
  
def build_sub_menu(parser, token):
    """
    {% submenu %}
    """
    return SubMenuObject()

class SubMenuObject(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        #current_path = context['request'].path
        #user = context['request'].user
        menu = False
        
        context['submenu_items'] = get_submenu_items(self)
        
        '''for m in Menu.objects.filter(base_url__isnull=False):
            if m.base_url and current_path.startswith(m.base_url):
                menu = m

        if menu:
            context['submenu_items'] = get_items(menu.slug, current_path, user)
            context['submenu'] = menu
        else:
            context['submenu_items'] = context['submenu'] = None
        return '' '''

def get_items(menu_name):
    """
    If possible, use a cached list of items to avoid continually re-querying 
    the database.
    The key contains the menu name, whether the user is authenticated, and the current path.
    Disable caching by setting MENU_CACHE_TIME to -1.
    """
    menuitems = AvailableModules.objects.prefetch_related('children').filter(level=menu_name,is_active=True,parent__isnull=True).only('name','base_url').order_by('order')
    return menuitems
    
def get_submenu_items(menu_name):
    try:submenuitems = AvailableModules.objects.filter(parent=menu_name).order_by('order')
    except:pass


def build_pages(parser, token):
    try:
       tag_name, page_name = token.split_contents()
    except:
       raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
    return PageObject(page_name)
    
class PageObject(template.Node):
    def __init__(self, page_name):
        self.page_name = page_name

    def render(self, context):
        context['pages'] = get_page_items(self.page_name)
        return ''
def get_page_items(page_name):
    pages = Pages.objects.only("name","slug").filter(is_static=True,is_active=True).order_by('id')
    return pages


register.tag('menu', build_menu)
register.tag('submenu', build_sub_menu)
register.tag('pages', build_pages)