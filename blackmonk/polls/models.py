import datetime
from datetime import date
import math,sys

from django.db import models
from common.models import Basetable


class Poll(Basetable):
    title = models.CharField(max_length = 350)
    slug = models.SlugField(null = True)
    expiry_date = models.DateField()
    is_single = models.BooleanField(max_length = 100)
    
    def get_choices(self):
        choices = Choices.objects.filter(poll=self.id)
        if choices:
            return choices
        else:
            return False 
    def expiry(self):
        today = datetime.datetime.now()
        y,m,d = str(self.expiry_date).split('-')
        d = datetime.date(int(y),int(m),int(d))
        remaining_days = d - today.date()
        return remaining_days.days
    
    def total_votes(self):
        total_vote = Choices.objects.filter(poll=self)
        vote=0
        for t in total_vote:
            vote += int(t.vote)
        return vote
    def result(self):
        results = []
        choice = Choices.objects.filter(poll=self).order_by('id')        
        total_votes = 0
        try:
            for c in choice:total_votes = total_votes + int(c.vote)
            for c in choice:
                vote_prcnt=(int(c.vote)*1.0/int(total_votes))*100
                results.append({'choice': c.choice, 'votes':c.vote, 'perc':int(vote_prcnt) })
        except:pass
        return results   
    
    def __unicode__(self):
        return self.title
    class Meta:
        permissions = (("publish_polls", "Can Publish Poll"),)
    
class Choices(models.Model):
    poll = models.ForeignKey(Poll,related_name="choices")
    choice = models.CharField(max_length = 350)
    vote = models.CharField(max_length=100,default=0)
    
    def get_percentage(self):
        total_vote = self.poll.total_votes()
        try:perc = (int(self.vote)*1.0/total_vote)*100
        except:
            perc = 0
        return perc
    
    def __unicode__(self):
        return self.choice
        
    

    
    
    
