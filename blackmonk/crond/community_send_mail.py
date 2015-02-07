import getsettings

from community.models import Topic, Entry
from datetime import datetime
from django.conf import settings as my_settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.template import RequestContext
from common.utils import get_global_settings

today_date = datetime.now().date()
global_settings = get_global_settings()

###############Topic Subscriber Email#######################
def topic_email(topic,message):
    for user in topic.subscriber.all():
        try:
            subject=topic.name+" Community Topics Updates!"
            email = EmailMessage(subject, message, my_settings.DEFAULT_FROM_EMAIL, ['anush@doublespring.com'])
            email.content_subtype = "html"
            email.send()
        except:
            pass

topic=None
email_template= 'default/community/community_email_template.html'
entries = Entry.objects.filter(created_on__day=today_date.day,created_on__month=today_date.month,created_on__year=today_date.year, status='P').order_by('topic__id')
topic_entrylist = []
for entry in entries:
    if topic is None:
        topic=entry.topic
    if topic == entry.topic:
        topic_entrylist.append(entry)
    else:
        topicmessage = render_to_string(email_template, {"entrylist": topic_entrylist,"topic":topic, "website_url": global_settings.website_url,"logo_url":global_settings.logo.url,"domain_name":global_settings.domain})
        topic_email(topic, message=topicmessage)
        topic_entrylist = [entry]
        topic=entry.topic
if topic_entrylist:
    topicmessage = render_to_string(email_template, {"entrylist": topic_entrylist,"topic":topic, "website_url": global_settings.website_url,"logo_url":global_settings.logo.url,"domain_name":global_settings.domain})
    topic_email(topic, message=topicmessage)
        
        
##################Question Subscriber Email#######################
def question_email(question, message):
    for user in question.subscriber.all():
        try:
            subject=question.title+" Community question Updates!"
            email = EmailMessage(subject, message, my_settings.DEFAULT_FROM_EMAIL, ['anush@doublespring.com'])
            email.content_subtype = "html"
            email.send()
        except:
            pass

question=None
email_template= 'default/community/community_email_template.html'
entries = Entry.objects.filter(created_on__day=today_date.day,created_on__month=today_date.month,created_on__year=today_date.year, status='P',entry_type='A').order_by('question__id')
appendlist = []
for entry in entries:
    if question is None:
        question=entry.question
    if question == entry.question:
        appendlist.append(entry)
    else:
        message = render_to_string(email_template, {"entrylist": appendlist,"question":question, "website_url": global_settings.website_url,"logo_url":global_settings.logo.url,"domain_name":global_settings.domain})
        question_email(question, message=message)
        question=entry.question
        appendlist = [entry]
if appendlist:
    message = render_to_string(email_template, {"entrylist": appendlist,"question":question, "website_url": global_settings.website_url,"logo_url":global_settings.logo.url,"domain_name":global_settings.domain})
    question_email(question, message=message)

