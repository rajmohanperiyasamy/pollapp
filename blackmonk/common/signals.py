from django.dispatch import Signal

create_staffmail = Signal(providing_args=["user","not_type"])
create_notification = Signal(providing_args=["object","module","action","user"])

celery_update_index = Signal(providing_args=["action","object"])
celery_update_indexs = Signal(providing_args=["action","objects"])
celery_delete_index = Signal(providing_args=["action","object"])
celery_delete_indexs = Signal(providing_args=["action","objects"])
