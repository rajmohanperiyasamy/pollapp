import datetime
from django.utils import timezone
from urlparse import urlparse

from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.template import RequestContext
from django.utils.encoding import smart_unicode
from django.db import settings
from django.utils.html import escape
from django.utils.translation import ugettext as _
from django.utils import dateformat
from django.template.defaultfilters import stringfilter
from django.conf import settings as my_settings
from django.contrib.contenttypes.models import ContentType


from common.models import MiscAttribute, CommonConfigure
from easy_thumbnails.files import get_thumbnailer

register = template.Library()

@register.filter
def content_type(obj):
    if not obj:
        return False
    return ContentType.objects.get_for_model(obj)

@register.simple_tag
def ds_markup(signature):
    signature=urlize(unicode(Markdown(signature, safe_mode='escape')))
    if signature:
        signature=urlize(unicode(Markdown(signature, safe_mode='escape')))
    else:
        return ''
    return signature
@register.filter
def ds_profile_link(user):
    data = u'<a href="%s">%s</a>' % (\
        reverse('forum_profile', args=[user.display_name]), user.display_name)
    return mark_safe(data)


@register.inclusion_tag('forum/pagination.html',takes_context=True)
def ds_pagination(context, label):
    page = context['page']
    paginator = context['paginator']
    return {'page': page,
            'paginator': paginator,
            'label': label,
            }

@register.filter
def ds_has_unreads(topic, user):
    """
    Check if topic has messages which user didn't read.
    """

    now = timezone.now()
    delta = datetime.timedelta(seconds=forum_settings.READ_TIMEOUT)

    if not user.is_authenticated():
        return False
    else:
        if isinstance(topic, Topic):
            if (now - delta > topic.updated):
                return False
            else:
                if hasattr(topic, '_read'):
                    read = topic._read
                else:
                    try:
                        read = Read.objects.get(user=user, topic=topic)
                    except Read.DoesNotExist:
                        read = None

                if read is None:
                    return True
                else:
                    return topic.updated > read.time
        else:
            raise Exception('Object should be a topic')


@register.filter
def forum_setting(name):
    return mark_safe(getattr(forum_settings, name, 'NOT DEFINED'))

@register.filter
def rstrip_cont(val):
    return val.rstrip()

@register.filter
def ds_moderated_by(topic, user):
    """
    Check if user is moderator of topic's forum.
    """

    return user.is_superuser or user in topic.forum.moderators.all()


@register.filter
def ds_editable_by(post, user):
    """
    Check if the post could be edited by the user.
    """

    if user.is_superuser:
        return True
    if post.user == user:
        return True
    if user in post.topic.forum.moderators.all():
        return True
    return False


@register.filter
def ds_posted_by(post, user):
    """
    Check if the post is writed by the user.
    """

    return post.user == user


@register.filter
def ds_equal_to(obj1, obj2):
    """
    Check if objects are equal.
    """

    return obj1 == obj2


@register.filter
def ds_unreads(qs, user):
    return cache_unreads(qs, user)
@register.tag
def ds_time(parser, token):
    try:
        tag, time = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('ds_time requires single argument')
    else:
        return DSTimeNode(time)
class DSTimeNode(template.Node):
    def __init__(self, time):
        self.time = template.Variable(time)

    def render(self, context):
        time = self.time.resolve(context)

        delta = timezone.now() - time
        today = timezone.now().replace(hour=0, minute=0, second=0)
        yesterday = today - datetime.timedelta(days=1)

        if delta.days == 0:
            if delta.seconds < 60:
                msg = _('seconds ago')
                return u'%d %s' % (delta.seconds, msg)

            elif delta.seconds < 3600:
                minutes = int(delta.seconds / 60)
                msg = _('minutes ago')
                return u'%d %s' % (minutes, msg)
        if time > today:
            return _('today, %s') % time.strftime("%I:%M %p")
        elif time > yesterday:
            return _('yesterday, %s') % time.strftime("%I:%M %p")
        else:
            return dateformat.format(time, 'd M, Y P ')

@register.simple_tag
def ds_link(object,link_class='', anchor=u''):
    """
    Return A tag with link to object.
    """

    url = hasattr(object,'get_absolute_url') and object.get_absolute_url() or None   
    anchor = anchor or smart_unicode(object)
    return mark_safe('<a href="%s" class="%s">%s</a>' % (url,link_class, escape(anchor)))

@register.filter
def twitter_time_search(start_time):
    start_time = datetime.datetime.strptime(start_time, "%a, %d %b %Y %H:%M:%S +0000")
    twitter_time = humanize_twitter_time(start_time)
    return twitter_time

@register.filter
def twitter_time_lists(start_time):
    start_time=datetime.datetime.strptime(start_time, "%a %b %d %H:%M:%S +0000 %Y")
    return humanize_twitter_time(start_time)


def humanize_twitter_time(start_time):
    start_time=start_time-datetime.timedelta(hours=7,minutes=1)
    delta = timezone.now() - start_time

    plural = lambda x: 's' if x != 1 else ''

    num_years = delta.days / 365
    if (num_years > 0):
        return "%d year%s ago" % (num_years, plural(num_years))

    num_weeks = delta.days / 7
    if (num_weeks > 0):
        return "%d week%s ago" % (num_weeks, plural(num_weeks))

    if (delta.days > 0):
        return "%d day%s ago" % (delta.days, plural(delta.days))

    num_hours = delta.seconds / 3600
    if (num_hours > 0):
        return "%d hour%s ago" % (num_hours, plural(num_hours))

    num_minutes = delta.seconds / 60
    if (num_minutes > 0):
        return "%d minute%s ago" % (num_minutes, plural(num_minutes))

    return "a few seconds ago"

@register.filter
def humanizeTimeDiff(start_time):
    delta = timezone.now() - start_time

    plural = lambda x: 's' if x != 1 else ''

    num_years = delta.days / 365
    if (num_years > 0):
        return "%d year%s ago" % (num_years, plural(num_years))

    num_weeks = delta.days / 7
    if (num_weeks > 0):
        return "%d week%s ago" % (num_weeks, plural(num_weeks))

    if (delta.days > 0):
        return "%d day%s ago" % (delta.days, plural(delta.days))

    num_hours = delta.seconds / 3600
    if (num_hours > 0):
        return "%d hour%s ago" % (num_hours, plural(num_hours))

    num_minutes = delta.seconds / 60
    if (num_minutes > 0):
        return "%d minute%s ago" % (num_minutes, plural(num_minutes))

    return "a few seconds ago"

@register.filter
def humanizeTimeDiff1(timestamp = None):
    """
    Returns a humanized string representing time difference
    between now() and the input timestamp.
    
    The output rounds up to days, hours, minutes, or seconds.
    4 days 5 hours returns '4 days'
    0 days 4 hours 3 minutes returns '4 hours', etc...
    """
    timeDiff = timezone.now() - timestamp
    days = timeDiff.days
    hours = timeDiff.seconds/3600
    minutes = timeDiff.seconds%3600/60
    seconds = timeDiff.seconds%3600%60
    
    str = ""
    tStr = ""
    if days > 0:
        if days == 1:   tStr = "day"
        else:           tStr = "days"
        str = str + "%s %s" %(days, tStr)
        return str
    elif hours > 0:
        if hours == 1:  tStr = "hour"
        else:           tStr = "hours"
        str = str + "%s %s" %(hours, tStr)
        return str
    elif minutes > 0:
        if minutes == 1:tStr = "min"
        else:           tStr = "mins"           
        str = str + "%s %s" %(minutes, tStr)
        return str
    elif seconds > 0:
        if seconds == 1:tStr = "sec"
        else:           tStr = "secs"
        str = str + "%s %s" %(seconds, tStr)
        return str
    else:
        return None

@register.filter
def twitter_add_link_username(text):
    import re
    r = re.compile(r"(@[^ |,|:|.|`|~|!|$|%|^|&|*|(|)|-|+|=|\|;|\"|<|>|?|\/]+)")
    index_at = r.sub(r'<a href="http://twitter.com/\1" target="_blank">\1</a>', text).replace('http://twitter.com/@','http://twitter.com/')
    return index_at

@register.filter
def twitter_add_link_trends(text):
    import re
    r = re.compile(r"(#[^ |,|:|.|`|~|!|$|%|^|&|*|(|)|-|+|=|\|;|\"|<|>|?|\/|_]+)")
    index_at = r.sub(r'<a href="http://search.twitter.com/search?q=\1" target="_blank">\1</a>', text).replace('http://search.twitter.com/search?q=#','http://search.twitter.com/search?q=%23')
    return index_at

@register.filter
def get_price_shortform(exact_price):
    from common.templatetags.currency import moneyfmt
    return moneyfmt(exact_price)
    '''
    exact_price = int(exact_price)
    price_shortform = ''
    crore = 10000000
    lac = 100000
    thousand = 1000
    if exact_price/crore > 0:
        price_shortform = str(exact_price/crore)
        temp_lac_price = exact_price - ((exact_price/crore)*crore)
        if temp_lac_price > 0:
            temp_lac_price = temp_lac_price/lac
            price_shortform += '.'+str(temp_lac_price)+' Cr'
        else:
            price_shortform += ' Cr'
    elif exact_price/lac > 0:
        price_shortform = str(exact_price/lac)
        temp_thousand_price = exact_price - ((exact_price/lac)*lac)
        if temp_thousand_price > 0:
            temp_thousand_price = temp_thousand_price/thousand
            price_shortform += '.'+ str(temp_thousand_price) +' Lac'
        else:
            price_shortform += ' Lac'
    elif exact_price/thousand > 0:
        price_shortform = str(exact_price/thousand) +',000'
    else:
        price_shortform = str(exact_price)
    return price_shortform
    '''

@register.filter
def is_added_within_a_week(date):
    try:
        import datetime
        today = timezone.now().date()
        posted_date = date.date()
        diff = today - posted_date
        posted_days =  diff.days
        if posted_days < 7:
            return True
        else:
            return False
    except:
         return False

@register.filter
def get_weather_date(date):
    try:
        date_obj=datetime.datetime.strptime(date,'%Y-%m-%d')
    except:
        date_obj=date    
    return date_obj   

@register.filter
def get_event_time(etime):
    import time
    from time import strptime
    try:
        new_time=datetime(*strptime(etime,"%H:%M:%S")[0:5])
        return new_time
    except:
        return etime
@register.filter    
def url_target_blank(text):
    try:
        return text.replace('<a ', '<a target="_blank" ')
    except:
        return text

@register.filter
def res_rating(value):
    try:
        value=str(value).split('.')
        temp=value[0]
        if int(value[1]) >=5:
            temp+='-5'
        return temp
    except:
        return value     

@register.filter
def buz_review_rating(value):
    try:
        value=value*20
        return temp
    except:
        return value  

@register.filter    
def remove_dirty_tags(bad_html):
    from bs4 import BeautifulSoup
    try:
        tree = BeautifulSoup(bad_html)
        good_html = tree.prettify()
    except:
        good_html = bad_html
    return good_html         

@register.filter 
def get_time_format(stime):
    import time
    try:
        stime = time.strptime(stime, "%H:%M:%S")
        return time.strftime("%I:%M %p",stime)
    except:
        return stime    

@register.simple_tag
def get_msg_class_name(value=None):
    
    """
        returns css class name for the respective message
    """
    if value=='s':return 'alert-success'
    elif value=='w':return 'alert-warn'
    elif value=='e':return 'alert-error'
    elif value=='i':return 'alert-info'
    else:return ''   

@register.simple_tag
def get_status_class(status=None):
    if status=='P':return 'published'
    elif status=='N':return 'pending'
    elif status=='B':return 'blocked'
    elif status=='R':return 'rejected'
    elif status=='E':return 'expired'
    elif status=='S':return 'scheduled'
    else:return 'drafted'
    
@register.simple_tag
def get_status_class_custom(status=None):
    if status=='P':return 'active'
    elif status=='B':return 'inactive'
    elif status=='S':return 'sold-out'
    else:return 'expired'   

@register.simple_tag
def get_notify_module(status=None):
    if status=='photo album':return 'photos'
    elif status=='article':return 'articles'
    elif status=='event':return 'events'
    else:return status    


@register.simple_tag
def get_social_fav_icon(url=None):
    if url:
        u = urlparse(url)
        icon= u.scheme+'://'+u.netloc+'/favicon.ico'
    return icon    
    """
    if media=='W':return my_settings.STATIC_URL+'ui/images/icons/e/26.png'
    elif media=='T':return 'http://www.twitter.com/favicon.ico'
    elif media=='F':return 'http://www.facebook.com/favicon.ico'
    elif media=='L':return 'http://www.linkedin.com/favicon.ico'
    elif media=='G':return 'http://plus.google.com/favicon.ico'
    """

@register.simple_tag
def split_show_times(showtime):
    rshowtimes=''
    try:
        st = showtime.split(',')
        
        for s in st:
            if s.strip() != '':
                rshowtimes+='<span>'+s+'</span>'
        st = rshowtimes  
        return st
    
    except:
        st = showtime
        return st    
    
@register.filter
def get_readable_time_format(date_time):     
    """
    converts a python datetime object to the 
    format "X days, Y hours ago"

    @param date_time: Python datetime object

    @return:
        fancy datetime:: string
    """
    try:
        current_datetime = timezone.now()
        delta = str(current_datetime - date_time)
    except:
        current_datetime = datetime.datetime.now()
        delta = str(current_datetime - date_time)
    if delta.find(',') > 0:
        days, hours = delta.split(',')
        days = int(days.split()[0].strip())
        hours, minutes = hours.split(':')[0:2]
    else:
        hours, minutes = delta.split(':')[0:2]
        days = 0
    days, hours, minutes = int(days), int(hours), int(minutes)
    datelets =[]
    years, months, xdays = None, None, None
    plural = lambda x: 's' if x!=1 else ''
    if days >= 365:
        years = int(days/365)
        datelets.append('%d year%s' % (years, plural(years)))
        days = days%365
    if days >= 30 and days < 365:
        months = int(days/30)
        datelets.append('%d month%s' % (months, plural(months)))        
        days = days%30
    if not years and days > 0 and days < 30:
        xdays =days
        datelets.append('%d day%s' % (xdays, plural(xdays)))        
    if not (months or years or days) and hours != 0:
        datelets.append('%dh' % (hours))        
    if not (xdays or months or years):
        datelets.append('%dm' % (minutes))        
    return ', '.join(datelets) 
      

@register.filter
def get_rating(value):
    value = value.split('.')
    if value[1] == '0':return str(value[0])
    else:return str(value[0] +'-'+ value[1])       

CURRENCY_CODES={'AUD':'AUD','USD':'$'}

@register.filter    
def get_currency_format(cur_code):
    try:return CURRENCY_CODES[cur_code]
    except:return cur_code
        
@register.simple_tag    
def get_misc_attribute(key=None):
    try:
        misc = MiscAttribute.objects.get(attr_key=key) 
        return misc.attr_value   
    except:None   
      
@register.assignment_tag
def seo_format_tag(*args, **kwargs):
    from common.models import SeoSettings, ModuleNames
    from common.utils import get_global_settings
    global_settings = get_global_settings()
    
    '''try:site_title = ModuleNames.get_module_seo(name='home')
    except:site_title  = None'''
    
    code = kwargs['code']
    title = kwargs['title']
    try:category = kwargs['category']
    except:category = False
    
    try:module_name = kwargs['module'].capitalize()
    except:module_name = False
    SEO_FORMAT_ORDER = {'T':title, 'N':global_settings.site_title, 'D':global_settings.domain, 'O':module_name, 'C':category}
    
    try:
        seo_format_obj = SeoSettings.objects.get(code=code)
        formated_seo = ''
        i=1
        for code in seo_format_obj.order:
            formated_seo += SEO_FORMAT_ORDER[code] 
            if i != len(seo_format_obj.order):
                formated_seo += ' | '
            i=i+1
        return formated_seo
    except:
        return title

ds_default_date = "%d/%b/%Y"
ds_default_time = "%I:%M %p"

@register.filter
def ds_site_dateformat(date):
    config=CommonConfigure.get_obj()
    if config.site_dateformat:
        try: return date.strftime(config.site_dateformat)
        except: return ''
    else:
        try: return date.strftime(ds_default_date)
        except: return ''
   

@register.filter
def ds_site_timeformat(date):
    config=CommonConfigure.get_obj()
    if config.site_timeformat:
        try: return date.strftime(config.site_timeformat)
        except: return ''
    else:
        try: return date.strftime(ds_default_time)
        except: return ''
    
@register.filter
def get_business_todays_working_hour(wh_obj):
    try:
        if timezone.now().strftime("%A") == 'Sunday':
            if wh_obj.sun_start:
                if wh_obj.sun_start == wh_obj.sun_end: work_hours = "open 24 hours"
                else: work_hours = wh_obj.sun_start.lower()+' - '+wh_obj.sun_end.lower()
            else:work_hours = 'Closed'
        elif timezone.now().strftime("%A") == 'Monday':
            if wh_obj.mon_start:
                if wh_obj.mon_start == wh_obj.mon_end: work_hours = "open 24 hours"
                else: work_hours = wh_obj.mon_start.lower()+' - '+wh_obj.mon_end.lower()
            else:work_hours = 'Closed'
        elif timezone.now().strftime("%A") == 'Tuesday':
            if wh_obj.tue_start:
                if wh_obj.tue_start == wh_obj.tue_end: work_hours = "open 24 hours"
                else: work_hours = wh_obj.tue_start.lower()+' - '+wh_obj.tue_end.lower()
            else:work_hours = 'Closed'
        elif timezone.now().strftime("%A") == 'Wednesday':
            if wh_obj.wed_start:
                if wh_obj.wed_start == wh_obj.wed_end: work_hours = "open 24 hours"
                else: work_hours = wh_obj.wed_start.lower()+' - '+wh_obj.wed_end.lower()
            else:work_hours = 'Closed'
        elif timezone.now().strftime("%A") == 'Thursday':
            if wh_obj.thu_start:
                if wh_obj.thu_start == wh_obj.thu_end: work_hours = "open 24 hours"
                else: work_hours = wh_obj.thu_start.lower()+' - '+wh_obj.thu_end.lower()
            else:work_hours = 'Closed'
        elif timezone.now().strftime("%A") == 'Friday':
            if wh_obj.fri_start:
                if wh_obj.fri_start == wh_obj.fri_end: work_hours = "open 24 hours"
                else: work_hours = wh_obj.fri_start.lower()+' - '+wh_obj.fri_end.lower()
            else:work_hours = 'Closed'        
        else:
            if wh_obj.sat_start:
                if wh_obj.sat_start == wh_obj.sat_end: work_hours = "open 24 hours"
                else: work_hours = wh_obj.sat_start.lower()+' - '+wh_obj.sat_end.lower()
            else:work_hours = 'Closed'  
    except:
        work_hours = False  
    return work_hours


@register.filter    
def subtract(value, arg):
    value= value - arg
    if value == 0:
        return ''
    else:
        return value

@register.filter
@stringfilter
def time_up_to(value, delimiter=None):
    try:return value.split(delimiter)[0]
    except:return value
time_up_to.is_safe = True    

@register.filter
def format_web_address(address):
    try:
        address = address.split('://')[1] 
    except: 
        address = address
    return address 

@register.filter
def get_transaction_date(date):
    transaction_date = date
    try:
        today = timezone.now().date()
        year = timezone.now().year
        if transaction_date.date() == today:
            return transaction_date.strftime('%I:%M %p')
        elif transaction_date.year == year:
            return transaction_date.strftime('%b %d')
        else:
            return transaction_date.strftime('%m/%d/%Y')
    except:
        return transaction_date.strftime('%m/%d/%Y')
    

@register.simple_tag
def get_module_percentage(number,posts):
    try:
        num = int(number)
        post = int(posts)
        return "%d%%" % (float(num) / post * 100)
    except:
        return '0%'

@register.filter
def remove_url_protocol(url):
    try:
        domain = url
        domain = domain.split('//')
        new_url = domain[1].rstrip('/')
    except:
        new_url = url
    return new_url
    
@register.inclusion_tag('default/image.html')
def get_image_block(**kwargs):
    from easy_thumbnails.files import get_thumbnailer
    data = {}
    image = kwargs.get('image', False)
    default_img = kwargs.get('default_img',False)
    data['image'] = image
    data['default_img'] = default_img
    data['class'] = kwargs.get('class','')
    data['icon_class'] = kwargs.get('icon_class','bUi-iCn-pHoT-24')
    data['size1'] = size1 = kwargs.get('size1','120x0')
    data['size2'] = size2 = kwargs.get('size2','200x0')
    data['size3'] = size3 = kwargs.get('size3','600x0')
    data['size4'] = size4 = kwargs.get('size4','300x0')
    data['size5'] = size5 = kwargs.get('size5','700x0')
    try:
        thumbnailer = get_thumbnailer(image)
         
        thumbnail_options = {'crop': True}
        num = 1
        for size in (size1, size2, size3, size4, size5):
            c_size = size.split('x')
            thumbnail_options.update({'size': (c_size[0], c_size[1])})
            thumb_img = thumbnailer.get_thumbnail(thumbnail_options)
            data['thumb_img%s'%num] = thumb_img
            num += 1
    except:pass
    data['url'] = kwargs.get('url', 'javascript:void(0);')
    data['title'] = kwargs.get('title','')
    return data

@register.filter
def is_portrait(image):
    portrait = False
    try:
        if image.width < image.height:
            portrait =  True
    except:
        pass
    return portrait

@register.filter
def get_iso_time_format(date_time):   
    try:iso = date_time.isoformat()
    except:iso = date_time
    return iso

@register.filter
def get_iso_time_duration(duration):
    iso_duration = 'TMS' 
    try:
        iso = duration.split(':')
        if iso[-1]:
            iso_duration = 'TM%sS'%iso[-1]
            if iso[-2]:
                iso_duration = 'T%sM%sS'%(iso[-2],iso[-1])
                if iso[-3]:
                    iso_duration = '%sT%sM%sS'%(iso[-3],iso[-2],iso[-1])
    except:pass
    return iso_duration
    
@register.assignment_tag
def get_payment_mode(id,type):
    from payments.models import PaymentOrder
    try:list = PaymentOrder.objects.filter(object_id=id,content_type__name=type,status='Success')[:1][0]
    except:list=None
    return list
          
@register.filter(name='split')
def split(value, arg):
    return value.split(arg)    