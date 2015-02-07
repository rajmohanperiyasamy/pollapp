import getsettings
import json

from usermgmt.models import EmailTemplates

data = open('emailtemplate.json') 
jsonData = json.load(data)
for x in jsonData:
    try:emailtemplate=EmailTemplates.objects.get(code=x['fields']['code'])
    except:emailtemplate=EmailTemplates(code=x['fields']['code'])
    emailtemplate.subject=x['fields']['subject']
    emailtemplate.template=x['fields']['template']
    emailtemplate.name=x['fields']['name']
    emailtemplate.save()

