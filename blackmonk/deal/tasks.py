import celery

from deal.models import Deal
from common.utils import date_fun

@celery.task(name='tasks.process_deal_expires')
def process_deal_expires():    
    deals = Deal.objects.filter(status='P', end_date__lte=date_fun()['today']).update(status='E')
    return "Success"