from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.db import DEFAULT_DB_ALIAS
from django.utils.importlib import import_module
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.validators import URLValidator
from django.contrib.auth import get_user_model

from common.models import AvailableApps,CommonConfigure,PaymentConfigure
#from usermgmt.models import Profile, ProfilePrivacy
User = get_user_model()

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Specifies the database to use. Default is "default".'),
    )
    help = "Dump data for Basic Models"

    requires_model_validation = False


    def handle(self, *args, **options):
        val = URLValidator()  # verify_exists=False
        user=User.objects.all()[0]
        try:config=CommonConfigure.objects.all()[0]
        except:config=CommonConfigure()    
        
        config.info_email=user.useremail
        
        config.site_title=raw_input('Enter Site Title : ')
        config.city=raw_input('Enter City Name : ')
        config.domain=raw_input('Enter Domain Name : ')
        config.country=raw_input('Enter Country Name : ')
        config.phone=raw_input('Enter Phone No : ')
        flag=True
        while flag:
            try:
                website_url=raw_input('Enter Website URL : ')
                val(website_url)
                config.website_url=website_url
                flag=False
            except:pass
        config.company_name=raw_input('Enter Company Name : ')
        config.company_address=raw_input('Enter Company Address : ')
        config.currency=raw_input('Enter Currency Symbol (eg:$) : ')[0]
        currency_code=raw_input('Enter Currency Code (eg:USD) : ')[:3]
        config.copyright=raw_input('Enter Copyright Content : ')
        config.info_email=raw_input('Enter info email : ')
        config.save()
        print "0000"
        try:payment_config=PaymentConfigure.objects.all[0]
        except:payment_config=PaymentConfigure()
        payment_config.currency_symbol=config.currency
        payment_config.currency_code=currency_code
        payment_config.save()
        
        try:site_url=config.website_url.split('http://')[1]
        except:site_url=config.website_url.split('https://')[1]
        
        site=Site.objects.all()[0]  
        site.name=config.domain
        site.domain=site_url
        site.save()
        
#        try:
#            profile = Profile.objects.get(user=user)
#        except:
#            profile = Profile(user=user,display_name=user.username)
#            profile.save()
#            privacy= ProfilePrivacy(profile=profile)
#            privacy.save()
        
        call_command('load_availableapps')
        for app in AvailableApps.objects.all().order_by('slug'):
            falg=True
            while falg:
                try:
                    text=str(app)+" :"
                    i=input(text)
                    if i==1:
                        app.status='A'
                        app.save()
                        falg=False
                    elif i==0:
                        app.status='N'
                        app.save()
                        falg=False
                except:pass
        
        call_command('load_data')
        return "-------------------Success-------------------\n"
