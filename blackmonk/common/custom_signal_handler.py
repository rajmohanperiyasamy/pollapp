from common.signals import celery_update_index,celery_update_indexs,celery_delete_index,celery_delete_indexs
from celery_haystack.utils import enqueue_task

def celery_update_index_handler(sender, **kwargs):
    try:enqueue_task(kwargs['object'].get_action_type(), kwargs['object'])
    except:pass
    
def celery_update_indexs_handler(sender, **kwargs):
    try:
        for object in kwargs['objects']:enqueue_task(object.get_action_type(), object)
    except:pass
        
def celery_delete_index_handler(sender, **kwargs):
    try:enqueue_task('delete', kwargs['object'])
    except:pass
    
def celery_delete_indexs_handler(sender, **kwargs):
    try:
        for object in kwargs['objects']:enqueue_task('delete', object)
    except:pass
        
celery_update_index.connect(celery_update_index_handler)
celery_update_indexs.connect(celery_update_indexs_handler)
celery_delete_index.connect(celery_delete_index_handler)
celery_delete_indexs.connect(celery_delete_indexs_handler)

"""
from common import signals


signals.celery_update_index.send(sender=None,object=business)
signals.celery_delete_index.send(sender=None,object=business)

signals.celery_update_indexs.send(sender=None,objects=business)
signals.celery_delete_indexs.send(sender=None,objects=business)

def get_action_type(self):
        if self.status=='P':return 'update'
        else:return 'delete'
"""    