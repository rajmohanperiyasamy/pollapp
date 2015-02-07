import datetime
from haystack import indexes
from bookmarks.models import Bookmark

"""
class BookmarkIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    def get_model(self):
        return Bookmark
    def index_queryset(self):
        return self.get_model().objects.filter(status='P')
"""