from django.template import Library
from article.models import Article
from django.core.cache import cache
CACHE_TIMEOUT=60*10
register = Library()

@register.assignment_tag
def get_latest_article(number):
    cache_key='cache_latestarticles'+str(number)
    latestarticles=cache.get('cache_latestarticles')
    if latestarticles is None:
        latestarticles = Article.objects.filter(status='P').only('title', 'content', 'slug', 'created_on', 'published_on', 'album').order_by('-id')[:number]
        cache.set(cache_key,latestarticles,CACHE_TIMEOUT)
    return latestarticles

@register.assignment_tag
def get_popular_article(number):
    cache_key='cache_populararticles'+str(number)
    populararticles=cache.get('cache_populararticles')
    if populararticles is None:
        populararticles = Article.objects.select_related('articlephotos').filter(is_active=True,status='P').only('title','created_on','published_on','slug').order_by('-most_viewed')[:5]
        cache.set(cache_key,populararticles,CACHE_TIMEOUT)
    return populararticles

@register.assignment_tag
def get_featured_article(limit):
    cache_key='cache_featuredarticle'+str(limit)
    featuredarticle=cache.get('cache_featuredarticle')
    if featuredarticle is None:
        featuredarticle = Article.objects.filter(status='P',featured=True).only('title', 'slug', 'created_on', 'published_on', 'created_by','album').select_related('created_by').order_by('-id')[:limit]
        cache.set(cache_key,featuredarticle,CACHE_TIMEOUT)
    return featuredarticle