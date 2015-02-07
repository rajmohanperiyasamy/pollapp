#! /home/blackmonk/virtualenvs/bm/bin/python
import getsettings
import datetime,time
from common.templatetags.ds_utils import get_misc_attribute
from south.models import MigrationHistory
from django.db import connection
from urlparse import urlparse
from meetup.models import MeetupSettings
import cgi
from domains import *


for domain in SCHEMATA_DOMAINS:
    connection.set_schemata_domain(domain)
    URL=get_misc_attribute('MEETUP_API')
    if not URL:
        continue
    parts= cgi.parse_qs(urlparse(URL).query)
    try:
        meetup = MeetupSettings.objects.all()[:1][0]
    except:
        meetup = MeetupSettings()
    meetup.city = parts['city'][0]
    meetup.lat = parts['lat'][0]
    meetup.lon = parts['lon'][0]
    meetup.state=  parts['state'][0]
    meetup.country = parts['country'][0]
    meetup.api_key = parts['key'][0]
    meetup.status = 'upcoming'
    meetup.save()
