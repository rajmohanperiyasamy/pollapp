import getsettings
import HTMLParser
from events.models import Event

pars = HTMLParser.HTMLParser()

def safe_it(text):
    text = pars.unescape(text)
    for tag in ['<p>', '</p>']:
        text = text.replace(tag, '')
    return "<p>" + text.strip() + "</p>"

def replace_invalid_chars():
    for evnt in Event.objects.all():
        evnt.seo_description = safe_it(evnt.seo_description)
        evnt.event_description = safe_it(evnt.event_description)
        evnt.save()

replace_invalid_chars()