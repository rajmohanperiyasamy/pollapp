from django.contrib.contenttypes.models import ContentType

def create_notification_handler(sender, **kwargs):
    try:
        from common.models import Notification
        notification = Notification()
        notification.user = kwargs['user']
        notification.content_object=kwargs['obj']
        notification.notification_type = kwargs['not_type']
        notification.object_title = kwargs.get('obj_title',None)
        notification.save()
    except:
        pass
    
from common.signals import create_notification
create_notification.connect(create_notification_handler)