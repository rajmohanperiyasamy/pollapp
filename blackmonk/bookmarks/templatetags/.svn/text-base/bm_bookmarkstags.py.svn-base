from django.template import Library
from bookmarks.models import Bookmark
register = Library()

@register.assignment_tag
def get_latest_bookmarks(limit=3):
    latest_bookmarks = Bookmark.objects.only("slug","title","summary","image_url").all().order_by('-id')[:limit]
    return latest_bookmarks
#register.simple_tag(get_latest_bookmarks)