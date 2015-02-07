from django.db.models import Q
from django.template import Library
from gallery.models import PhotoAlbum, Photos
from django.core.cache import cache
CACHE_TIMEOUT=60*10
register = Library()

@register.assignment_tag
def get_featured_albums(limit=4):
    cache_key='ttag_featured_gallery_pack'+str(limit)
    fetched_values = ['title','slug','published_on','created_by']
    featured_gallery_pack=cache.get(cache_key)
    if featured_gallery_pack is None:
        featured_gallery_pack = {}
        featured_gallery_pack['main_featured_album'] = main_featured_album = PhotoAlbum.objects.prefetch_related('album_photos').select_related('created_by').only(*fetched_values).filter(status='P',is_featured=True).order_by('-id')[:1]
        featured_gallery_pack['featured_albums'] = PhotoAlbum.objects.prefetch_related('album_photos').only('title','slug').filter(status='P',is_featured=True).exclude(id__in = main_featured_album).order_by('-id')[:limit]
        cache.set(cache_key,featured_gallery_pack,CACHE_TIMEOUT)
    return featured_gallery_pack

@register.assignment_tag
def get_featured_photos(limit):
    cache_key='ttag_featured_photos'+str(limit)
    featured_photos=cache.get(cache_key)
    if featured_photos is None:
        featured_photos = Photos.objects.only('photo','photo_url','album','created_by').filter(album__status='P',album__is_featured=True,album__category__is_editable=True).select_related('album','created_by').order_by('album__id').distinct('album__id')[:limit]
        cache.set(cache_key,featured_photos,CACHE_TIMEOUT)
    return featured_photos

@register.assignment_tag
def get_latest_gallery(**kwargs):
    limit = kwargs.get('limit', 5)
    category = kwargs.get('category', False)
    album = kwargs.get('album_obj', None)
    if category:photoalbums = PhotoAlbum.objects.only('title','slug','category','most_viewed','published_on').filter(category = category,status='P').exclude(id = album.id).prefetch_related('album_photos').select_related('category').order_by('-id')[:limit]
    else:photoalbums = PhotoAlbum.objects.only('title','slug','category','most_viewed','published_on').filter(status='P').exclude(id = album.id).prefetch_related('album_photos').select_related('category').order_by('-id')[:limit]
    return photoalbums
    
@register.assignment_tag
def get_trending_gallery(**kwargs):
    limit = kwargs.get('limit', 5)
    category = kwargs.get('category', False)
    album = kwargs.get('album_obj', None)
    if category:photoalbums = PhotoAlbum.objects.only('title','slug','category','most_viewed','published_on').filter(category = category,status='P').exclude(id = album.id).prefetch_related('album_photos').select_related('category').order_by('-most_viewed')[:limit]
    else:photoalbums = PhotoAlbum.objects.only('title','slug','category','most_viewed','published_on').filter(status='P').exclude(id = album.id).prefetch_related('album_photos').select_related('category').order_by('-most_viewed')[:limit]
    return photoalbums

@register.assignment_tag
def get_related_gallery(**kwargs):
    limit = kwargs.get('limit', 12)
    category = kwargs.get('category', False)
    album = kwargs.get('album_obj', None)
    if category:photoalbums = PhotoAlbum.objects.only('title','slug','category','most_viewed','published_on').filter(Q(tags__in = album.tags.all()) | Q(category = category),status='P').exclude(id = album.id).prefetch_related('album_photos').select_related('category').distinct().order_by('-most_viewed')[:limit]
    else:photoalbums = PhotoAlbum.objects.only('title','slug','category','most_viewed','published_on').filter(tags__in = album.tags.all(), status='P').exclude(id = album.id).prefetch_related('album_photos').select_related('category').order_by('-most_viewed')[:limit]
    return photoalbums



