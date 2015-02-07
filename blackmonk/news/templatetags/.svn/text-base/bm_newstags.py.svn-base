from news.models import News
from django.template import Library
register = Library()

@register.assignment_tag
def get_news_list(limit=9):
    news_list = News.objects.only("title","slug").all().order_by('-modified_on')[:limit]
    return news_list