import sys
import getsettings
from usermgmt.models import EmailTemplates

def getallapps():
	allapps=EmailTemplates.objects.all().order_by('name')
	template = "{0:2}|{1:30}|{2:20}|{3:6}|{4:4}|{5:40}"
	print " =========================================================================================================================================" 
	print template.format("| ID", "NAME","TYPE", "STATUS", "CODE","SUBJECT ")
	print template.format("|===", "==============================", "====================", "======", "====","=====================================================================")
	for app in allapps:
		print "|",template.format(app.id,app.name,app.type,app.active,app.code,app.subject)
	print " ========================================================================================================================================="
print "__________________________________________________________________________________________________________________________________________\n"
try:
	if len(sys.argv)==1:getallapps()
	elif len(sys.argv)==2:
		if sys.argv[1]!='update':print "Please type update to add/edit Email template,del id to delete"
		if sys.argv[1]=='update':
			name=type=active=code=subject=template=''
			id=raw_input('enter id(leave blank if adding new template):')
			while name=='':name=raw_input('enter name:')
			while type=='':type=raw_input('enter type:')
			while active not in [1,0]:active=input('enter active status(1/0):')
			while code=='':code=raw_input('enter code:')
			subject=raw_input('enter subject:')
			template=raw_input('enter template:')
			
			try:
				etemp=EmailTemplates.objects.get(id=id)
				etemp.name=name
				etemp.type=type
				etemp.active=active
				etemp.code=code
				new=False
				print "Updating Available Apps..."
			except:
				print "Inserting to Available Apps..."
				etemp=EmailTemplates(name=name,type=type,active=active,code=code)
				new=True
			if new:
				etemp.subject=subject
				etemp.template=template
			etemp.save()
			print "=================================================================Success================================================================="
			getallapps()
	elif len(sys.argv)==3:
		if sys.argv[1]=='DEL' or sys.argv[1]=='del':
			flag=raw_input('Are you sure want to delete it y/n:')
			if flag=='y':
				print "Deleting EmailTemplate Apps..."
				app=EmailTemplates.objects.get(id=int(sys.argv[2]))
				app.delete()
				print "=================================================================Deleted================================================================="
			else:print "=================================================================Canceled================================================================="
		getallapps()
except:
	import sys
	print "Error : ",sys.exc_info()
print "__________________________________________________________________________________________________________________________________________"

