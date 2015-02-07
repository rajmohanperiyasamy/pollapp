from django.template import Library
from datetime import date
from deal.models import Deal, DealCategory, Faqs
register = Library()

@register.assignment_tag
def get_current_featured_deals(limit=4):
    featured_deal = Deal.objects.filter(status='P',featured = True,end_date__gte=date.today(), start_date__lte=date.today()).order_by('-created_on')[:limit]
    return featured_deal

@register.assignment_tag
def get_deal_categories(limit=2):
    categories = DealCategory.objects.only('name','slug').order_by('name')
    return categories

@register.assignment_tag
def get_related_deals(**kwargs):
    key = {}
    limit = kwargs.get('limit', 6)
    category = kwargs.get('category', False)
    deal = kwargs.get('deal', None)
    key['status'] = 'P'
    key['category'] = category
    key['end_date__gte'] = date.today()
    key['start_date__lte'] = date.today()
    deals = Deal.objects.only('title','slug').filter(**key).exclude(id = deal.id).order_by('-created_on')[:limit]
    return deals

@register.assignment_tag
def get_deals_faqs():
    return Faqs.objects.all().order_by('id')

@register.assignment_tag
def get_home_page_featured_deals(limit=1):
    fetched_values = ['title','slug','about','original_price','discount_price','end_date','start_date','album']
    today = date.today()
    featured_deals = Deal.objects.select_related('album').only(*fetched_values).filter(status='P',featured = True, end_date__gte=today, start_date__lte=today).order_by('-created_on')[:limit]
    return featured_deals
    