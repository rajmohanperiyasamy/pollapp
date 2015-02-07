import getsettings
from django.contrib.sites.models import Site
from common.models import CommonConfigure
from django.db import connection
from domains import *
def update_site_name():
    common_config=CommonConfigure.get_obj()
    try:
        sites=Site.objects.all()[0]
        sites.name=common_config.domain
        sites.domain=common_config.website_url.split('://')[1]
        sites.save()

    except:
        import sys
        print "Error :"+sys.exc_info()
for domain_name  in SCHEMATA_DOMAINS:
    connection.set_schemata_domain(domain_name)  
    update_site_name()


