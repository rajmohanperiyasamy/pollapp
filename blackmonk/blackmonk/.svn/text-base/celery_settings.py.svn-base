from celery.schedules import crontab
CELERYBEAT_SCHEDULE = {
    'business_expires': {
        'task': 'tasks.process_business_expires',
        'schedule': crontab(minute=0, hour=0)
    },
    'process_classifieds_expires': {
        'task': 'tasks.process_classifieds_expires',
        'schedule': crontab(minute=1, hour=0)
    },
    'process_deal_expires': {
        'task': 'tasks.process_deal_expires',
        'schedule': crontab(minute=2, hour=0)
    },
    'process_event_expires': {
        'task': 'tasks.process_event_expires',
        'schedule': crontab(minute=3, hour=0)
    },
    'process_polls_expires': {
        'task': 'tasks.process_polls_expires',
        'schedule': crontab(minute=4, hour=0)
    },
    'process_sweepstakes_expires_select_winners': {
        'task': 'tasks.process_sweepstakes_expires_select_winners',
        'schedule': crontab(minute=5, hour=0)
    },
    'useremail_validate': {
        'task': 'tasks.process_user_emailvalidate',
        'schedule': crontab(minute=6, hour=0)
    },
    'process_analytics_data': {
        'task': 'tasks.process_analytics_data',
        'schedule': crontab(minute=8, hour=0)
    }, 
    'news_feed': {
        'task': 'tasks.news_feed',
        'schedule': crontab(minute=10,hour='*/2')
    },
    'process_clear_session': {
        'task': 'tasks.clear_session',
        'schedule': crontab(minute=1, hour=1)
    },                  
    
}

CELERY_TIMEZONE = 'UTC'
