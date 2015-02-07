from django.template import Library
from flowers.models import Category
register = Library()

@register.assignment_tag
def get_flower_categories(type='parent'):
    if type == 'parent':
        categories = Category.objects.filter(parent__isnull=True).order_by('id')
    else:
        categories = Category.objects.filter(parent__isnull=False).order_by('name')
    return categories        
    

