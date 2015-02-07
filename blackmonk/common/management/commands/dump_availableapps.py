from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS
from django.utils.importlib import import_module

from common.models import AvailableApps
from common.dump_load_utils import common_dump_data

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Specifies the database to use. Default is "default".'),
    )
    help = "Dump data for Basic Models"

    requires_model_validation = False


    def handle(self, *args, **options):
        try:
            COMMON_TABLE_LIST=[{'file_name':'common_AvailableApps.json','model':AvailableApps,'filter':{}}]
            common_dump_data(COMMON_TABLE_LIST)
            status_out="-------------------Success-------------------\n"
        except:
            import sys
            status_out=str(sys.exc_info())+'\n'
        return status_out