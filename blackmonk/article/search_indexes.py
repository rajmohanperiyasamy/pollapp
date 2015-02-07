from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex
from article.models import Article


class ArticleIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title', boost=9)
    status = indexes.CharField(model_attr='status')
    order_date=indexes.DateTimeField(model_attr='published_on',null=True)
    description=indexes.CharField(model_attr='summary',null=True)
    
    def get_model(self):
        return Article
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(status='P')
    def should_update(self, instance, **kwargs):
        if instance.status=='P':return True
        else:return False
    """    
    def prepare(self, obj):
        data = super(ArticleIndex, self).prepare(obj)
        data['boost'] = 0.5
        return data
    """
    