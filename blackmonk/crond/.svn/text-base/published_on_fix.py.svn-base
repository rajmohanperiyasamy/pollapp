import getsettings

from classifieds.models import Classifieds
from gallery.models import PhotoAlbum
from videos.models import Videos

for c in Classifieds.objects.all():
    c.published_on=c.created_on
    c.save()
for c in PhotoAlbum.objects.all():
    c.published_on=c.created_on
    c.save()
for c in Videos.objects.all():
    c.published_on=c.created_on
    c.save()
