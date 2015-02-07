from mailsnake import MailSnake
from mailsnake.exceptions import *
from django.http import HttpResponse 
from common.models import NewsLetterApiSettings
from django.conf import settings as my_settings


def subscripe_newsletter(name,email):
    try:
        ms = MailSnake(my_settings.MAILCHAMP_API_KEY)
        dd={"FNAME":name}
        ms.listSubscribe(apikey=my_settings.MAILCHAMP_API_KEY, id=my_settings.MAILCHAMP_LIST_ID, email_address=email,merge_vars=dd,email_type='html',double_optin=False,update_existing=False, replace_interests=True,send_welcome=True)
    except:
        pass

    
def ajax_subscripe_newsletter(name,email,mailtype='html'):
    nws_ltr_obj = NewsLetterApiSettings.objects.all()[:1][0]
    if nws_ltr_obj.option == 'MC':
        try:
            ms = MailSnake(nws_ltr_obj.api_key)
            dd={"FNAME":name}
            ms.listSubscribe(apikey=nws_ltr_obj.api_key, id=nws_ltr_obj.list_id, email_address=email,merge_vars=dd,email_type=mailtype,double_optin=False,update_existing=False, replace_interests=True,send_welcome=True)
            return HttpResponse('1')
        except ListAlreadySubscribedException:return HttpResponse('2')
        except:return HttpResponse('0')
    else:return HttpResponse('0')   