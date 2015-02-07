import mptt

from django.db import models
from django.contrib.comments.models import Comment

from mptt_comments.managers import MpttCommentManager

class MpttComment(Comment):
    title = models.CharField(max_length=255,null=True)
    like = models.IntegerField(max_length=4,null=True,default=0)
    dislike = models.IntegerField(max_length=4,null=True,default=0)
    flag = models.IntegerField(max_length=4,null=True,default=0)
    rating= models.DecimalField(max_digits=4, decimal_places=2,null=True,default=0)
    
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True)
    class Meta:
        ordering = ('tree_id', 'lft')
    
    objects = MpttCommentManager()

mptt.register(MpttComment)
from mptt_comments.signals import * 
