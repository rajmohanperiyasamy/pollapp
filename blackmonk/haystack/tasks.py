import celery
import time

from haystack.management.commands import update_index,clear_index

@celery.task(name='tasks.celery_rebuild_index')
def celery_rebuild_index():
    celery.current_task.update_state(state="PROGRESS")
    clear_index.Command().handle(yes_or_no='y')
    time.sleep(10)
    update_index.Command().handle()
    return "Success"