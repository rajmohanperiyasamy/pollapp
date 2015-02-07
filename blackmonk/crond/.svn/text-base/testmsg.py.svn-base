import getsettings

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core import mail
from django.conf import settings as my_settings
from django.template import  Template,Context
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage


import requests
import urllib2,urllib



URL='http://biz.smsbox.ch:10015/723/sms/xml'
datax="<?xml version='1.0' encoding='UTF-8' ?><SMSBoxXMLRequest><username>wrs10921</username><password>ESRJNX69</password><command>WEBSEND</command><parameters><receiver>+918884329411</receiver><service>WRS</service><text>This is a message from World Radio Switzerland!</text><guessOperator/></parameters></SMSBoxXMLRequest>"

"""
response = urllib.urlopen(URL)
print response.read()
"""

from httplib2 import Http
from urllib import urlencode
h = Http()
#data = 'Test'
data = dict(name="Joe", comment="A test comment")
resp, content = h.request("http://biz.smsbox.ch:10015/723/sms/xml", "POST", urlencode(data))
resp

