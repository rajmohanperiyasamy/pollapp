from django.template import Library
from videos.models import VideoCategory, Videos
from django.core.cache import cache
CACHE_TIMEOUT=60*10
register = Library()

@register.assignment_tag
def get_featured_videos(limit=20):
    cache_key='ttag_featured_video_pack'+str(limit)
    featured_video_pack=cache.get(cache_key)
    if featured_video_pack is None:
        featured_video_pack = {}
        featured_video_pack['featured_videos'] = featured_videos = Videos.objects.only("title","slug","video_id").filter(status='P',featured=True).order_by('-id')[:limit]
        featured_video_pack['main_featured_video'] = Videos.objects.filter(status='P',featured=True).exclude(id__in=featured_videos).order_by('-id')[:1]
        cache.set(cache_key,featured_video_pack,CACHE_TIMEOUT)
    return featured_video_pack 

@register.assignment_tag
def get_featured_videos_by_category(**kwargs):
    fetched_values = ['title','slug','video_id','is_vimeo','vimeo_image','published_on','video_view','duration','category']
    limit = kwargs.get('limit', 20)
    category = kwargs.get('category', False)
    if category:featured_videos = Videos.objects.only(*fetched_values).filter(category = category,status='P',featured=True).order_by('-id')[:limit]
    else:featured_videos = Videos.objects.only(*fetched_values).filter(status='P',featured=True).order_by('-id')[:limit]
    return featured_videos

@register.assignment_tag
def get_video_categories():
    cache_key='ttag_video_categories'
    video_categories=cache.get(cache_key)
    if video_categories is None:
        video_categories=VideoCategory.objects.all().order_by('name')
        cache.set(cache_key,video_categories,CACHE_TIMEOUT)
    return video_categories
@register.assignment_tag
def get_latest_videos(**kwargs):
    limit = kwargs.get('limit', 5)
    category = kwargs.get('category', False)
    videoid = kwargs.get('videoid', None)
    if category:videos = Videos.objects.only('title','slug','video_id','is_vimeo','vimeo_image','published_on','video_view','duration').filter(category = category,status='P').exclude(id = videoid).order_by('-id')[:limit]
    else:videos = Videos.objects.only('title','slug','video_id','is_vimeo','vimeo_image','published_on','video_view','duration').filter(status='P').exclude(id = videoid).order_by('-id')[:limit]
    return videos
    
@register.assignment_tag
def get_trending_videos(**kwargs):
    limit = kwargs.get('limit', 5)
    category = kwargs.get('category', False)
    videoid = kwargs.get('videoid', None)
    if category:videos = Videos.objects.only('title','slug','video_id','is_vimeo','vimeo_image','published_on','video_view','duration').filter(category = category,status='P',video_view__gte=10).exclude(id = videoid).order_by('-video_view')[:limit]
    else:videos = Videos.objects.only('title','slug','video_id','is_vimeo','vimeo_image','published_on','video_view','duration').filter(status='P',video_view__gte=10).exclude(id = videoid).order_by('-video_view')[:limit]
    return videos    

@register.assignment_tag
def get_related_videos(**kwargs):
    limit = kwargs.get('limit', 15)
    video = kwargs.get('video_obj', None)
    videos = Videos.objects.only('title','slug','video_id','is_vimeo','vimeo_image','published_on','video_view','duration').filter(category = video.category, status='P').exclude(id = video.id).order_by('-video_view')[:limit]
    return videos  
    