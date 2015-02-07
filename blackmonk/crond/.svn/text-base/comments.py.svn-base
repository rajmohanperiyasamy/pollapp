import getsettings
from django.contrib.contenttypes.models import ContentType
from mptt_comments.models import MpttComment


print "_______________________________________________________________________________________________\n"
try:
	c_type=MpttComment.objects.values('content_type')
	alist=[]
	for c in c_type:
		if not c['content_type'] in alist:alist.append(c['content_type'])
	for id in alist:
		c_obj=MpttComment.objects.filter(content_type__id=id,level__gte=1).order_by('lft')
		model=ContentType.objects.get_for_id(id)
		for comment in c_obj:
			try:
				obj=model.get_object_for_this_type(id=comment.object_pk)
			except:
				print "Deleting Comment"
				try:comment.delete()
				except:pass
except:
	import sys
	print "Error : ",sys.exc_info()
print "_______________________________________________________________________________________________"

