from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS
from django.utils.importlib import import_module

from common.models import AvailableApps

APPS=[
      "advice","article","attraction","bookmarks","business","buzz","common","classifieds","deal","events",
      "forum","gallery","jobs","meetup","movies","news","usermgmt","videos","sweepstakes"
    ]

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Specifies the database to use. Default is "default".'),
    )
    help = "Load data for Basic Models"

    requires_model_validation = False


    def handle(self, *args, **options):
        status_out="-------------------Success-------------------\n"
        #APPS=[app.slug for app in AvailableApps.objects.filter(status='A')]
        try:app_name=args[0] 
        except:app_name='all'
        if app_name=='all':
            for app in APPS:
                module = import_module('%s.dump_load' % (app))
                module.load_data()
        elif app_name in APPS:
            module = import_module('%s.dump_load' % (app_name))
            module.load_data()
        else:
            status_out="Error : Please enter valid module name(or leave blank to load all the modules).\n"
        return status_out
    