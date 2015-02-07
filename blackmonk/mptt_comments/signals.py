from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.contrib.contenttypes.models import ContentType

from mptt_comments.models import MpttComment

from article.models import Article
from attraction.models import Attraction
from business.models import Business
from classifieds.models import Classifieds
from events.models import Event
from movies.models import Movies
from gallery.models import Photos
from videos.models import Videos

@receiver(post_delete, sender=Article)
def _mymodel_delete(sender, instance, **kwargs):
    comments=MpttComment.objects.filter(content_type=ContentType.objects.get_for_model(instance),object_pk=instance.id)
    comments.delete()
    
@receiver(post_delete, sender=Attraction)
def _mymodel_delete(sender, instance, **kwargs):
    comments=MpttComment.objects.filter(content_type=ContentType.objects.get_for_model(instance),object_pk=instance.id)
    comments.delete()

@receiver(post_delete, sender=Business)
def _mymodel_delete(sender, instance, **kwargs):
    comments=MpttComment.objects.filter(content_type=ContentType.objects.get_for_model(instance),object_pk=instance.id)
    comments.delete()
    
@receiver(post_delete, sender=Classifieds)
def _mymodel_delete(sender, instance, **kwargs):
    comments=MpttComment.objects.filter(content_type=ContentType.objects.get_for_model(instance),object_pk=instance.id)
    comments.delete()

@receiver(post_delete, sender=Event)
def _mymodel_delete(sender, instance, **kwargs):
    comments=MpttComment.objects.filter(content_type=ContentType.objects.get_for_model(instance),object_pk=instance.id)
    comments.delete()
    
@receiver(post_delete, sender=Movies)
def _mymodel_delete(sender, instance, **kwargs):
    comments=MpttComment.objects.filter(content_type=ContentType.objects.get_for_model(instance),object_pk=instance.id)
    comments.delete()

@receiver(post_delete, sender=Photos)
def _mymodel_delete(sender, instance, **kwargs):
    comments=MpttComment.objects.filter(content_type=ContentType.objects.get_for_model(instance),object_pk=instance.id)
    comments.delete()
    
@receiver(post_delete, sender=Videos)
def _mymodel_delete(sender, instance, **kwargs):
    comments=MpttComment.objects.filter(content_type=ContentType.objects.get_for_model(instance),object_pk=instance.id)
    comments.delete()
