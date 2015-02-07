import celery

from polls.models import Poll
from common.utils import date_fun

@celery.task(name='tasks.process_polls_expires')
def process_polls_expires():
    polls = Poll.objects.filter(status='P', expiry_date__lt=date_fun()['today'])
    if polls:
        polls.update(status='E')
        try:
            current_poll = Poll.objects.filter(status='N', expiry_date__gte=date_fun()['today'])[0]
            current_poll.status = 'P'
            current_poll.save()
        except:pass
    return "Success"