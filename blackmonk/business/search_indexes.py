from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex
from business.models import Business


class BusinessIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='name', boost=9)
    status = indexes.CharField(model_attr='status')
    order_date=indexes.DateTimeField(model_attr='created_on')
    description=indexes.CharField(model_attr='description',null=True)
    
    def get_model(self):
        return Business
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(status='P')
    def should_update(self, instance, **kwargs):
        if instance.status=='P':return True
        else:return False
    """    
    def prepare(self, obj):
        data = super(BusinessIndex, self).prepare(obj)
        data['boost'] = 0.5
        return data
    """