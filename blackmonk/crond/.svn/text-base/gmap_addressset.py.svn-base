import sys
import getsettings
import time
from googlemaps import GoogleMaps
from common.models import Address
from domains import *
from django.db import connection
connection.set_schemata_domain('127.0.0.1')
for addrs in Address.objects.filter(map_zoom__isnull=True):
    time.sleep(1)
    gmaps = GoogleMaps()
    print "addr"
    print addrs.address1
    address = addrs.address1+" ,"+addrs.city
    try:
         lat, lng = gmaps.address_to_latlng(address)
    except:
        print "No found lat long"
        print addrs.address1
        continue
    if lat and lng:
        addrs.lat= lat
        addrs.lon= lng
        addrs.map_zoom= 13
        addrs.save()
    else:
        print "No lat long"
        print addrs.address1