from django.core.mail import EmailMessage
from django.conf import settings as my_settings
from django.template.loader import render_to_string
from django.template import RequestContext

MODULES={
        'community':'Community',
        'articles':'Article',
        'business':'Business',
        'bookmarks':'Bookmark',
        'classifieds':'Classified',
        'discussions':'Discussion',
        'events':'Event',
        'photos':'Gallery/Photos',
        'videos':'Video',
        'deals':'Deal',
        'banners':'Banners'
}

def create_staffmail_handler(sender, **kwargs):
    try:
        from common.utils import get_global_settings
        from common.models import StaffEmailSettings
        mail=True
        if kwargs['action']=='UG':
            kwargs['action']='U'
            upgrade=True
        else:upgrade=False
        try:staffmail=StaffEmailSettings.objects.get(availableapps__name__iexact=kwargs['module'],action=kwargs['action'])
        except:
            mail=False
        if mail:
            global_settings = get_global_settings()
            
            subject='Notification from '+global_settings.domain
            to_email=staffmail.emails.split(',')
            
            if kwargs['action']=='A':
                if kwargs['module'] == 'community':
                    type = {'Q':'Question','A':'Answer','P':'Post'}[kwargs['object'].entry_type]
                    if type=='Answer':
                        action='Answer added to Question'
                    else:
                        action='Added a '+type
                else:action='Added a '+MODULES[kwargs['module']]
            elif kwargs['action']=='C':action='Claiming a '+MODULES[kwargs['module']]
            elif kwargs['action']=='P':action='Purchased a '+MODULES[kwargs['module']]
            else:
                if kwargs['module']=='community':
                    type = {'Q':'Question','A':'Answer','P':'Post'}[kwargs['object'].entry_type]
                    action='Updated a '+type 
                else:
                    if upgrade:action='Upgraded a '+MODULES[kwargs['module']]
                    else:action='Updated a '+MODULES[kwargs['module']]
            
            mail_data={}
            if kwargs['module']=='community' and kwargs['action']=='U':mail_data['obj_title']=kwargs['object'].title
            else:mail_data['obj_title']=kwargs['object']
            mail_data['action']=action
            mail_data['usr']=kwargs['user']
            mail_data['url']=global_settings.website_url+kwargs['object'].get_preview_url()
            mail_data['updatedon']=kwargs['object'].get_modified_time()
            email_message = render_to_string("staff_mail.html",mail_data)
            email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_email)
            email.content_subtype = "html"
            email.send()
    except:
        pass
    
from common.signals import create_staffmail
create_staffmail.connect(create_staffmail_handler)