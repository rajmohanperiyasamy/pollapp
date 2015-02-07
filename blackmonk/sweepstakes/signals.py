from django.db.models.signals import post_delete,post_save
from django.dispatch.dispatcher import receiver
from django.contrib.contenttypes.models import ContentType

from sweepstakes.models import Sweepstakes,SweepstakesPoints,SweepstakesParticipant,SweepstakesParticipantPoints

from community.models import Entry 
# from MpttComment.models import MpttComment as Community_Comment
from article.models import Article
from bookmarks.models import Bookmark
from business.models import Business
from classifieds.models import Classifieds
#from forum.models import Topic,Post
from events.models import Event
from gallery.models import Photos
from videos.models import Videos
from mptt_comments.models import MpttComment
#########from deals.models import##########

def process_app_point(instance,user,app_slug):
    contest=SweepstakesParticipant.objects.get(participant=user,status='A')
    points=SweepstakesPoints.objects.get(sweepstake=contest,app__slug=app_slug).app_point
    if points:
        user=SweepstakesParticipantPoints(content_object=instance,sweepstakes=contest)
        user.user_point=points
        user.save()
        contest.total=contest.total+points
        contest.save()
    return True

def process_extra_app_point(instance,user,app_slug):
    contest=SweepstakesParticipant.objects.get(participant=user,status='A')
    points=0
    if app_slug=='advice':points=contest.advice_e
    if app_slug=='discussions':points=contest.discussions_e
    if app_slug=='comments':points=contest.comments
    if points:
        user=SweepstakesParticipantPoints(content_object=instance,sweepstakes=contest)
        user.user_point=points
        user.save()
        contest.total=contest.total+points
        contest.save()
    return True
    
#########################################################################
#########################################################################
#########################################################################

@receiver(post_save, sender=Entry)
def _mymodel_save(sender, instance, **kwargs):
    try:
        if kwargs['created']:process_app_point(instance,instance.created_by,'advice')
    except:pass

@receiver(post_save, sender=Article)
def _mymodel_save(sender, instance, **kwargs):
    try:
        if kwargs['created']:process_app_point(instance,instance.created_by,'articles')
    except:pass

@receiver(post_save, sender=Bookmark)
def _mymodel_save(sender, instance, **kwargs):
    try:
        if kwargs['created']:process_app_point(instance,instance.created_by,'bookmarks')
    except:pass

@receiver(post_save, sender=Business)
def _mymodel_save(sender, instance, **kwargs):
    try:
        if kwargs['created']:process_app_point(instance,instance.created_by,'business')
    except:pass
    
@receiver(post_save, sender=Classifieds)
def _mymodel_save(sender, instance, **kwargs):
    try:
        if kwargs['created']:process_app_point(instance,instance.created_by,'classifieds')
    except:pass

# @receiver(post_save, sender=Topic)
# def _mymodel_save(sender, instance, **kwargs):
#     try:
#         if kwargs['created']:process_app_point(instance,instance.created_by,'discussions')
#     except:pass

@receiver(post_save, sender=Event)
def _mymodel_save(sender, instance, **kwargs):
    try:
        if kwargs['created']:process_app_point(instance,instance.created_by,'events')
    except:pass
    
@receiver(post_save, sender=Photos)
def _mymodel_save(sender, instance, **kwargs):
    try:
        if kwargs['created']:process_app_point(instance,instance.created_by,'photos')
    except:pass
    
@receiver(post_save, sender=Videos)
def _mymodel_save(sender, instance, **kwargs):
    try:
        if kwargs['created']:process_app_point(instance,instance.created_by,'videos')
    except:pass

#########################################################################
#########################################################################
#########################################################################

@receiver(post_save, sender=Entry)
def _mymodel_save(sender, instance, **kwargs):
    try:
        if kwargs['created']:process_extra_app_point(instance,instance.created_by,'advice')
    except:pass

# @receiver(post_save, sender=Entry)
# def _mymodel_save(sender, instance, **kwargs):
#     try:
#         if kwargs['created']:
#             topic=Topic.objects.get(id=instance.topic)
#             if topic.post_count > 1:process_extra_app_point(instance,instance.created_by,'discussions')
#     except:pass

#########################################################################
#########################################################################
#########################################################################
# 
# @receiver(post_save, sender=Community_Comment)
# def _mymodel_save(sender, instance, **kwargs):
#     try:
#         if kwargs['created']:process_extra_app_point(instance,instance.created_by,'comments')
#     except:pass

@receiver(post_save, sender=MpttComment)
def _mymodel_save(sender, instance, **kwargs):
    try:
        if kwargs['created']:process_extra_app_point(instance,instance.created_by,'comments')
    except:pass
