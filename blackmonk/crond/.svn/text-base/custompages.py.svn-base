import sys
import getsettings

from django.template.defaultfilters import slugify

from common.models import Pages
from common.getunique import getUniqueValue

def getallpages():
    allapps=Pages.objects.all().order_by('name')
    template = "{0:2}|{1:20}|{2:20}|{3:7}|{4:4}"
    print " ============================================================= " 
    print template.format("| ID", "NAME", "SLUG", "STATIC", "ACTIVE |")
    print template.format("|===", "====================", "====================", "=======", "=======|")
    for app in allapps:
        print "|",template.format(app.id,app.name,app.slug,app.is_static,app.is_active),'  |'
    print " ============================================================="
print "_______________________________________________________________________________________________\n"
try:
    if len(sys.argv)==1:getallpages()
    elif len(sys.argv)==2:
        if sys.argv[1]=='update':
            name=slug=active=static=''
            id=input('enter id:')
            while name=='':name=raw_input('enter name:')
            while slug=='':slug=raw_input('enter slug:')
            while active not in [1,0]:active=input('enter active status(1/0):')
            while static not in [1,0]:static=input('enter static status(1/0):')
            
            try:
                print "Updating Custom pages..."
                page=Pages.objects.get(id=id)
                page.slug=getUniqueValue(Pages,slugify(slug),instance_pk=page.id)
                page.name=name
                page.is_static=static
                page.is_active=active
                page.save()
            except:
                import sys
                print "Error : ",sys.exc_info()
            print "==================================Success=================================="
            getallpages()
        else:
            print "Invalid input give update-id,name(char),slug(char),active(1/0),static(1/0) or del id"    
    elif len(sys.argv)==3:
        if sys.argv[1]=='DEL' or sys.argv[1]=='del':
            flag=raw_input('Are you sure want to delete it y/n:')
            if flag=='y':
                print "Deleting Available Apps..."
                app=Pages.objects.get(id=int(sys.argv[2]))
                app.delete()
                print "==================================Deleted=================================="
            else:print "==================================Canceled=================================="
        getallpages()
except:
    import sys
    print "Error : ",sys.exc_info()
print "_______________________________________________________________________________________________"


    