import sys
import getsettings
from django.template.defaultfilters import slugify
from common.models import AvailableApps
from common.getunique import getUniqueValue
from django.db import connection
from django.conf import settings
#Comment below block if running locally#
#start#
domain_name=raw_input('enter domain:')
if domain_name not in settings.SCHEMATA_DOMAINS:
	print "invalid domain"
	exit()
connection.set_schemata_domain(domain_name)
#end#
def getallapps():
	allapps=AvailableApps.objects.all().order_by('name')
	template = "{0:2}|{1:20}|{2:20}|{3:7}"
	print " ========================================================== " 
	print template.format("| ID", "NAME", "SLUG", "STATUS")
	print template.format("|===", "====================", "====================", "=======", "====|")
	for app in allapps:
		print "|",template.format(app.id,app.name,app.slug,app.status),'  |'
	print " =========================================================="
print "_______________________________________________________________________________________________\n"
try:
	if len(sys.argv)==1:getallapps()
	elif len(sys.argv)==2:
		if sys.argv[1]=='update':
			flag=True
			while flag:
				name=raw_input('enter name:')
				if name!='':flag=False
				
			flag=True
			while flag:
				slug=raw_input('enter slug:')
				if slug!='':flag=False
				
			flag=True
			while flag:
				status=raw_input('enter status(A/I/N):')
				if status in ['A','I','N']:flag=False
				
			
			
			try:
				app=AvailableApps.objects.get(name__iexact=name)
				print "Updating Available Apps..."
				update=True
			except:
				print "Inserting to Available Apps..."
				app=AvailableApps()
				update=False
			app.name=name
			if update:
				app.slug=getUniqueValue(AvailableApps,slugify(slug),instance_pk=app.id)
			else:
				app.slug=getUniqueValue(AvailableApps,slugify(slug))
			app.status=status
			
			app.save()
			print "==================================Success=================================="
			getallapps()
		else:
			try:
				val=sys.argv[1].split(',')
				flag=True
				if not val[2] in ['A','I','N']:flag=False
				if not int(val[3]) in [1,0]:flag=False
				if flag:
					try:
						app=AvailableApps.objects.get(name__iexact=val[0])
						print "Updating Available Apps..."
					except:
						print "Inserting to Available Apps..."
						app=AvailableApps()
					app.name=val[0]
					app.slug=val[1]
					app.status=val[2]
					app.save()
					print "==================================Success=================================="
					getallapps()
				else:
					print "Invalid input give status(A/I/N),app(1/0)"
			except:
				print "Invalid input give name(char),slug(char),status(A/I/N),app(1/0) or update"	
	elif len(sys.argv)==3:
		if sys.argv[1]=='DEL' or sys.argv[1]=='del':
			flag=raw_input('Are you sure want to delete it y/n:')
			if flag=='y':
				print "Deleting Available Apps..."
				app=AvailableApps.objects.get(id=int(sys.argv[2]))
				app.delete()
				print "==================================Deleted=================================="
			else:print "==================================Canceled=================================="
		getallapps()
except:
	import sys
	print "Error : ",sys.exc_info()
print "_______________________________________________________________________________________________"

