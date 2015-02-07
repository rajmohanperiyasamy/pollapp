from photo_library.signals import photo_submit
from photo_library.models import * 

def photo_submit_handler(sender, **kwargs):

    photo = PhotoLibrary()
    photo.created_by = kwargs['user']
    photo.photo_url = kwargs['url']
    photo.tags = kwargs.get('tags',None)
    photo.summary = kwargs.get('summary',None)
    photo.is_staff = kwargs.get('is_staff',True)
    photo.save()
    
    

photo_submit.connect(photo_submit_handler)