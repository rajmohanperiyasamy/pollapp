#! /home/blackmonk/virtualenvs/bm/bin/python
import getsettings
import json
from django.db import connection
from jobs.models import JobCategory
from common.utils import get_global_settings
from django.core import serializers
from django.core.management.color import no_style
from domains import *
for domain_name  in SCHEMATA_DOMAINS:
    connection.set_schemata_domain(domain_name)
    globalsettings=get_global_settings()
    data = open('jbs.json') 
    #jsonData = json.load(data)
    for obj in serializers.deserialize("json", data):
        djobj = obj.object
        djobj.seo_title=djobj.seo_title.replace('Onlinewinnipeg.com',globalsettings.domain).replace('Winnipeg',globalsettings.city)
        djobj.seo_description=djobj.seo_description.replace('Onlinewinnipeg.com',globalsettings.domain).replace('Winnipeg',globalsettings.city)
        djobj.save()
    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [JobCategory])
    if sequence_sql:
        print("Resetting sequence")
        cursor = connection.cursor()
        for command in sequence_sql:
            cursor.execute(command)
    
        
    """
    globalsettings=get_global_settings()
    data = open('jbs.json') 
    jsonData = json.load(data)
    for x in jsonData:
        try:
            category=JobCategory.objects.get(code=x['fields']['name'])
            continue
        except:
            category=JobCategory(name=x['fields']['name'])
            category.key=x['fields']['key']
            category.slug=x['fields']['slug']
            category.seo_title=x['fields']['seo_title']
            category.seo_description=x['fields']['seo_description']
            category.seo_title=category.seo_title.replace('Onlinewinnipeg.com',globalsettings.domain).replace('Winnipeg',globalsettings.city)
            category.seo_description=category.seo_description.replace('Onlinewinnipeg.com',globalsettings.domain).replace('Winnipeg',globalsettings.city)
            category.save()
    data.close()
    """
