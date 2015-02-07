from django.db import models

class Meetup(models.Model):
    name = models.CharField(max_length=250)
    url = models.CharField(max_length=250)
    photo = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    venue = models.CharField(max_length=250)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    event_date = models.DateTimeField()
    rsvp = models.IntegerField()
    group_name = models.CharField(max_length=250)
    group_url  = models.CharField(max_length=400)
    
    class Meta:
        abstract = True
        
class MeetupSettings(models.Model):
    city  = models.CharField(max_length=100)
    zip  = models.CharField(max_length=10,null=True,blank=True)
    state  = models.CharField(max_length=50)
    country  = models.CharField(max_length=50)
    lat  = models.FloatField(null=True,blank=True)
    lon  = models.FloatField(null=True,blank=True)
    radius  = models.IntegerField(default=25)
    status  = models.CharField(max_length=100)
    api_key  = models.CharField(max_length=100)
    
    
class MeetupTopics(models.Model):
    topic   = models.CharField(max_length=100)
    slug    = models.CharField(max_length=120)
    
    def __unicode__(self):
        return self.topic