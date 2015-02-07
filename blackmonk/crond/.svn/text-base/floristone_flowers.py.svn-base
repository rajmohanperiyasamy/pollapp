#! /home/blackmonk/virtualenvs/bm/bin/python
 # -*- coding: utf-8 -*-

import getsettings
from django.contrib.auth import get_user_model
User = get_user_model()
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_str
from domains import *
from common.getunique import getUniqueValue
from flowers.models import FlowerApiSettings,Category,Flowers

import suds
from suds.client import Client

from django.db import connection

def __fetch_flower_details(api_settings):
    furl="https://www.floristone.com/webservices4/flowershop.cfc?wsdl"
    client = Client(furl)
    admin = User.objects.get(id=1)
    categories = Category.objects.filter(parent__isnull=False).order_by('id')
    
    for cat in categories:
        result = client.service.getProducts(str(api_settings.api_key), str(api_settings.api_password), str(cat.code.strip()), "100", "1")
        for product in result.products:
            try:
                flower_obj = Flowers.objects.get(flower_code = str(product.code))
            except:
                flower_obj = Flowers(created_by=admin,flower_code = str(product.code))
            try:
                flower_obj.name = str(product.name.decode('utf-8'))
                flower_obj.name = str(flower_obj.name.encode('ascii', 'xmlcharrefreplace'))
            except:flower_obj.name = smart_str(product.name)
            flower_obj.slug = getUniqueValue(Flowers,slugify(flower_obj.name),instance_pk=flower_obj.id)
            #flower_obj.category = cat
            try:
                flower_obj.description = str(product.description.decode('utf-8'))
                flower_obj.description = str(flower_obj.description.encode('ascii', 'xmlcharrefreplace'))
            except:flower_obj.description = smart_str(product.description)  
            flower_obj.price = float(product.price)
            flower_obj.image_large = str(product.image)
            flower_obj.image_thumbnail = str(product.thumbnail)
            flower_obj.is_active = True
            flower_obj.save()
            flower_obj.categories.add(cat) 
            
try:
    api_settings = FlowerApiSettings.objects.all()[:1][0]
except:pass

Flowers.objects.all().delete()
__fetch_flower_details(api_settings)            
