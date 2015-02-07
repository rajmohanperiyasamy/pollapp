import getsettings

from django.template.defaultfilters import slugify

from common.getunique import getUniqueValue
from common.models import VenueType

venue_types = (
              ('', '-- Select Venue Type --'),
              ('Arena/Stadium', 'Arena/Stadium'),
              ('Bar/Club', 'Bar/Club'),
              ('Beach', 'Beach'),
              ('Coffeehouse', 'Coffeehouse'),
              ('College', 'College'),
              ('Gallery', 'Gallery'),
              ('Hotel', 'Hotel'),
              ('Landmark/Attraction', 'Landmark/Attraction'),
              ('Museum', 'Museum'),
              ('Nightlife', 'Nightlife'),
              ('Organization/Community Agency', 'Organization/Community Agency'),
              ('Park', 'Park'),
              ('Performance Theater', 'Performance Theater'),
              ('Place of Worship', 'Place of Worship'),
              ('Others', 'Others')
              )

def create_venue_type():
    for key,value in venue_types:
        if key!='':
            try:
                VenueType.objects.get(title__iexact=key)
            except:
                venuetype=VenueType(title=key,seo_title=key,seo_description=key)
                venuetype.slug=getUniqueValue(VenueType,slugify(key))
                venuetype.save()

def change_venue_type():
    for venue in Address.objects.all():
        venuetype=VenueType.objects.get(title__iexact=venue.type)
        venue.type=venuetype.id
        venue.save()
        
                
create_venue_type()
change_venue_type()