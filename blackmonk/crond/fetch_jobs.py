#! /home/blackmonk/virtualenvs/bm/bin/python
import getsettings
from common.getunique import *
from django.template.defaultfilters import slugify
from jobs.models import JobCategory,JobTitle,JobCompany,JobDetail,JobSettings
from common.models import *
from common.utils import get_global_settings
from django.db import models
import datetime,time,urllib2
from time import strptime
from datetime import timedelta
from xml.etree import ElementTree 
from django.db import connection
from domains import *
#for domain_name  in SCHEMATA_DOMAINS:


def getText(nodelist):
   rc = ""
   for node in nodelist:
       if node.nodeType == node.TEXT_NODE:
           rc = rc + node.data
   return rc

def get_date(in_date):
    stime = time.strptime(in_date[:10],'%Y-%m-%d')
    return datetime.datetime(*stime[0:5])

def get_api_url(cat,page):
    jobs=JobSettings.objects.all()[:1][0]
    url = jobs.jurl
    url = '%sq-%s/pn=%s'%(url,cat,page)
    if jobs.location:
        url = '%s/l-%s'%(url,jobs.location) 
        
    url = '%s?pshid=%s&ssty=%s&cflg=%s&jbd=%s'%(url,jobs.pshid,jobs.ssty,jobs.cflg,jobs.jbd)    
        
    return url

def get_jobs():
    cmp_date = datetime.datetime.now()-timedelta(1)
    user = User.objects.get(id=1)
    category = JobCategory.objects.all().order_by('id')
    for cat in category:
        for page in range(1,2):
            url = get_api_url(cat.key,page)
            request = urllib2.Request(url, headers={"Accept" : "application/xml"})
            xml = urllib2.urlopen(request)
            tree = ElementTree.parse(xml)
            rootElem = tree.getroot()
            job_list = rootElem.find('rs').findall("r")  
            
            for job in job_list:
                job_obj = JobDetail(is_active=True)
                
                try:cmp_obj = JobCompany.objects.get(company=job.findtext("cn").strip())
                except:cmp_obj = JobCompany(company=job.findtext("cn").strip())
                cmp_obj.count = cmp_obj.count+1
                cmp_obj.save()
                
                try:title_obj = JobTitle.objects.get(title=job.findtext("jt").strip())
                except:title_obj = JobTitle(title=job.findtext("jt").strip())
                title_obj.count = title_obj.count+1
                title_obj.save()
    
                job_obj.category = cat
                job_obj.title = title_obj
                job_obj.company = cmp_obj
                job_obj.source = job.findtext("src")
                job_obj.source_url = job.find("src").attrib.get('url')
                job_obj.detail = job.findtext("e")
                job_obj.type = job.findtext("ty")
                job_obj.location = job.findtext("loc")
                job_obj.slug = getUniqueValue(JobDetail,slugify(title_obj.title[:25]))
                job_obj.created_by = user
                job_obj.modified_by = user
                job_obj.active_on = get_date(job.findtext("ls"))
                if job_obj.active_on >= cmp_date:
                    job_obj.status = 'N'
                job_obj.save()
            
for domain_name  in SCHEMATA_DOMAINS:
    connection.set_schemata_domain(domain_name)
    try:
         jobs=JobSettings.objects.all()[:1][0]
    except:
        continue
    JobDetail.objects.all().delete()
    JobCompany.objects.all().update(count=0)
    JobTitle.objects.all().update(count=0)
   
    
            
