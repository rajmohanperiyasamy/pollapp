import base64
from cgi import escape
import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache as _djcache
from django.core.paginator import Paginator
from django.db.models.signals import pre_delete
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from googlemaps import GoogleMaps
from hashlib import sha1
import hashlib
from heapq import nlargest
import hmac
from itertools import repeat, ifilter
from operator import itemgetter
import os
from pygeocoder import Geocoder
import time
from xhtml2pdf import pisa
from xml.sax.saxutils import unescape

import cStringIO as StringIO
from common.models import CommonConfigure
import json as simplejson
from common.models import ContactEmails

NUMBER_DISPLAYED = 5
NUMBER_DISPLAYED_DASH = 10

LEADING_PAGE_RANGE_DISPLAYED = TRAILING_PAGE_RANGE_DISPLAYED =8
LEADING_PAGE_RANGE = TRAILING_PAGE_RANGE = 5
NUM_PAGES_OUTSIDE_RANGE = 2
ADJACENT_PAGES = 1


escape_dict = {
    "&lsquo;": "'",
    "&rsquo;": "'",
    "&sbquo;": ",",
    "&ldquo;": '"',
    "&rdquo;": '"',
    "&bdquo;": ",,",
    "&oline;": "-",
    "&#09;": "    ",
    "&nbsp;": " ",
    "&#10;": " ",          
    "&#32;": " ",
    "&#33;": "!",
    "&#34;": '"',
    "&quot;": '"',
    "&#35;": "#",
    "&#36;": "$",
    "&#37;": "%",
    "&#38;": "&",    
    "&amp;": "&",
    "&#39;": "'",
    "&#40;": "(",
    "&#41;": ")",
    "&#42;": "*",
    "&#43;": "+",
    "&#44;": ",",
    "&#45;": "-",
    "&#46;": ".",
    "&#47;": "/",    
    "&frasl;": "/",
    "&#58;": ":",
    "&#59;": ";",
    "&#60;": "<",
    "&lt;": "<",
    "&#61;": "=",
    "&#62;": ">",    
    "&gt;": ">",
    "&#63;": "?",
    "&#64;": "@",
    "&#91;": "[",
    "&#92;": "\\",
    "&#93;": "]",
    "&#94;": "^",
    "&#95;": "_",
    "&#96;": "`",
    "&#8216;": "'",
    "&#8217;": "'",
    "%u02DC": "~",
    "%u2013": "-",
    "%u2014": "-",
    "%u2018": "'",
    "%u2019": "'",
    "%u201A": ",",
    "%u201C": '"',
    "%u201D": '"',
    "%u201E": '"',
    "%u2026": "...",
    "%u2030": "%",
    "%u2032": "'",
    "%u2033": '"',
    "%u2039": "<",
    "%u203A": ">",
}

def ds_cleantext(text):
    return unescape(text, escape_dict).strip()

sort_dict={'F':1,'S':2,"B":3}
def sort_queryset(lt):
    if lt:
        return sort_dict[lt]
    else:
        return 4

def ds_sortby_listingtype(bm_model):
    try:
        if bm_model.__name__ == 'Event': 
            sorted_objects = bm_model.objects.extra(select={'Featured': "listing_type = 'F'", 'Sponsored': "listing_type = 'S'", 'Basic': "listing_type = 'B'"})
            sorted_objects = sorted_objects.extra(order_by = ['Basic', 'Sponsored', 'Featured', '-start_date'])
        elif bm_model.__name__ == 'Business':
            sorted_objects = bm_model.objects.extra(select={'Featured': "featured_sponsored = 'F'", 'Sponsored': "featured_sponsored = 'S'", 'Basic': "featured_sponsored = 'B'"})
            sorted_objects = sorted_objects.extra(order_by = ['Basic', 'Sponsored', 'Featured'])
    except:
        sorted_objects = bm_model.objects.all()
    return sorted_objects

def ds_pagination(objects,page,temp_var,result_per_page):
    
    paginator = Paginator(objects, result_per_page)
    count = paginator.count

    in_leading_range = in_trailing_range = False
    pages_outside_leading_range = pages_outside_trailing_range = range(0)
    (pages) = paginator.num_pages
    if pages<page:
        page=1
    if (pages <= LEADING_PAGE_RANGE_DISPLAYED):
        in_leading_range = in_trailing_range = True
        page_numbers = [n for n in range(1, pages + 1) if n > 0 and n <= pages]
    elif (page+1 <= LEADING_PAGE_RANGE):
        in_leading_range = True
        page_numbers = [n for n in range(1, LEADING_PAGE_RANGE_DISPLAYED - NUM_PAGES_OUTSIDE_RANGE +1) if n > 0 and n <= pages]
        pages_outside_leading_range = [n + pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
    elif (page+1 > pages - TRAILING_PAGE_RANGE):
        in_trailing_range = True
        page_numbers = [n for n in range(pages - TRAILING_PAGE_RANGE_DISPLAYED + NUM_PAGES_OUTSIDE_RANGE +1 , pages + 1) if n > 0 and n <= pages]
        pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
    else: 
        page_numbers = [n for n in range(page - ADJACENT_PAGES, page+1 + ADJACENT_PAGES +1) if n > 0 and n <= pages]
        pages_outside_leading_range = [n + pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
        pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]

    paginator2 = paginator.page(page)
    if pages==1:
        is_paginated = False
    else:
        is_paginated = True
    from_range= ((page-1)*result_per_page) + 1   
    if paginator2.has_next():
        to_range=page*result_per_page
    else:
        to_range=count
    next_page_number = previous_page_number = None 
    try:
        next_page_number = paginator2.next_page_number()
    except: pass
    try:
        previous_page_number = paginator2.previous_page_number()
    except: pass
    data = {            
            'count':count,
            'page':page,
            'pages':pages,
            'from_range':from_range,
            'to_range':to_range,
            'results_per_page': result_per_page,
            'is_paginated': is_paginated,
            'current_page':page,
             temp_var:paginator2.object_list,
            'next':next_page_number,
            'prev':previous_page_number,
            'has_next':paginator2.has_next(),
            'has_previous':paginator2.has_previous(),
            'page_numbers': page_numbers,
            'in_leading_range': in_leading_range,
            'in_trailing_range': in_trailing_range,
            'pages_outside_leading_range': pages_outside_leading_range,
            'pages_outside_trailing_range': pages_outside_trailing_range
            
            }
    return data

def get_global_settings():
    
    from common.models import CommonConfigure
    settings = CommonConfigure.get_obj()
    return settings

def get_ad_settings():
    from common.models import Advertisement
    settings = Advertisement.get_obj()
    return settings
    
def get_lat_lng(a):
    global_settings = get_global_settings()
    try:
        a = a[1:len(a)-1]
        a = a.split(',')
        return [float(a[0]), float(a[1]), global_settings.google_map_zoom]
    except:
        return [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]


def fetch_resources(uri, rel):
   
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT,
                            uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        
        path = os.path.join(settings.STATIC_MEDIA_ROOT,
                            uri.replace(settings.STATIC_URL, ""))
    else:
        return uri

    return path

    
def render_to_pdf(template_src, context_dict,filename):
        global_settings = get_global_settings()
        template = get_template(template_src)
        context_dict['STATIC_URL']=settings.STATIC_URL
        context_dict['MEDIA_URL']=settings.MEDIA_URL
        context_dict['globalsettings']=global_settings
        context = Context(context_dict)
        html  = template.render(context)
        result = StringIO.StringIO()
    
        pdf =  pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                                                dest=result,
                                                encoding='UTF-8',link_callback=fetch_resources)
        if not pdf.err:
            response = HttpResponse(result.getvalue(), mimetype='application/pdf')
            response['Content-Disposition'] = 'filename=%s'%(filename)
            return response
        return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
    
    
    

       

class Counter(dict):
    '''Dict subclass for counting hashable objects.  Sometimes called a bag
    or multiset.  Elements are stored as dictionary keys and their counts
    are stored as dictionary values.

    >>> Counter('zyzygy')
    Counter({'y': 3, 'z': 2, 'g': 1})

    '''

    def __init__(self, iterable=None, **kwds):
        '''Create a new, empty Counter object.  And if given, count elements
        from an input iterable.  Or, initialize the count from another mapping
        of elements to their counts.

        >>> c = Counter()                           # a new, empty counter
        >>> c = Counter('gallahad')                 # a new counter from an iterable
        >>> c = Counter({'a': 4, 'b': 2})           # a new counter from a mapping
        >>> c = Counter(a=4, b=2)                   # a new counter from keyword args

        '''        
        self.update(iterable, **kwds)

    def __missing__(self, key):
        return 0

    def most_common(self, n=None):
        '''List the n most common elements and their counts from the most
        common to the least.  If n is None, then list all element counts.

        >>> Counter('abracadabra').most_common(3)
        [('a', 5), ('r', 2), ('b', 2)]

        '''        
        if n is None:
            return sorted(self.iteritems(), key=itemgetter(1), reverse=True)
        return nlargest(n, self.iteritems(), key=itemgetter(1))

    def elements(self):
        '''Iterator over elements repeating each as many times as its count.

        >>> c = Counter('ABCABC')
        >>> sorted(c.elements())
        ['A', 'A', 'B', 'B', 'C', 'C']

        If an element's count has been set to zero or is a negative number,
        elements() will ignore it.

        '''
        for elem, count in self.iteritems():
            for _ in repeat(None, count):
                yield elem

    # Override dict methods where the meaning changes for Counter objects.

    @classmethod
    def fromkeys(cls, iterable, v=None):
        raise NotImplementedError(
            'Counter.fromkeys() is undefined.  Use Counter(iterable) instead.')

    def update(self, iterable=None, **kwds):
        '''Like dict.update() but add counts instead of replacing them.

        Source can be an iterable, a dictionary, or another Counter instance.

        >>> c = Counter('which')
        >>> c.update('witch')           # add elements from another iterable
        >>> d = Counter('watch')
        >>> c.update(d)                 # add elements from another counter
        >>> c['h']                      # four 'h' in which, witch, and watch
        4

        '''        
        if iterable is not None:
            if hasattr(iterable, 'iteritems'):
                if self:
                    self_get = self.get
                    for elem, count in iterable.iteritems():
                        self[elem] = self_get(elem, 0) + count
                else:
                    dict.update(self, iterable) # fast path when counter is empty
            else:
                self_get = self.get
                for elem in iterable:
                    self[elem] = self_get(elem, 0) + 1
        if kwds:
            self.update(kwds)

    def copy(self):
        'Like dict.copy() but returns a Counter instance instead of a dict.'
        return Counter(self)

    def __delitem__(self, elem):
        'Like dict.__delitem__() but does not raise KeyError for missing values.'
        if elem in self:
            dict.__delitem__(self, elem)

    def __repr__(self):
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)

    # Multiset-style mathematical operations discussed in:
    #       Knuth TAOCP Volume II section 4.6.3 exercise 19
    #       and at http://en.wikipedia.org/wiki/Multiset
    #
    # Outputs guaranteed to only include positive counts.
    #
    # To strip negative and zero counts, add-in an empty counter:
    #       c += Counter()

    def __add__(self, other):
        '''Add counts from two counters.

        >>> Counter('abbb') + Counter('bcc')
        Counter({'b': 4, 'c': 2, 'a': 1})


        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] + other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __sub__(self, other):
        ''' Subtract count, but keep only results with positive counts.

        >>> Counter('abbbc') - Counter('bccd')
        Counter({'b': 2, 'a': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        result = Counter()
        for elem in set(self) | set(other):
            newcount = self[elem] - other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __or__(self, other):
        '''Union is the maximum of value in either of the input counters.

        >>> Counter('abbb') | Counter('bcc')
        Counter({'b': 3, 'c': 2, 'a': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        _max = max
        result = Counter()
        for elem in set(self) | set(other):
            newcount = _max(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result

    def __and__(self, other):
        ''' Intersection is the minimum of corresponding counts.

        >>> Counter('abbb') & Counter('bcc')
        Counter({'b': 1})

        '''
        if not isinstance(other, Counter):
            return NotImplemented
        _min = min
        result = Counter()
        if len(self) < len(other):
            self, other = other, self
        for elem in ifilter(self.__contains__, other):
            newcount = _min(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result


def custom_cache(seconds = 900):
    def doCache(f):
        def x(*args, **kwargs):
                key = sha1(str(f.__module__) + str(f.__name__) + str(args) + str(kwargs)).hexdigest()
                result = _djcache.get(key)
                if result is None:
                    result = f(*args, **kwargs)
                    _djcache.set(key, result, seconds)
                return result
        return x
    return doCache

@custom_cache(600)
def date_fun():
    today=datetime.date.today()
    return {
            'today':today,
            "three_days_after":today + relativedelta(days= +3),
            "thirthy_days_before": today + relativedelta(days= -30),
            "cmp_date": datetime.datetime.now() - datetime.timedelta(3)
            }

def get_map_lat_lng_zoom(latt,lon,zoom, add1, add2, zip, city):
    globalsettings = get_global_settings()
    LAT, LON, ZOOM = 0,0,0
    try:
        ZOOM = int(zoom)
    except:
        ZOOM = 11
    try:
        LAT = float(latt)
        LON = float(lon)
    except:
        try:
            gmaps = GoogleMaps()
            address = add1+','+add2+','+zip+','+city
            LAT, LON = Geocoder.geocode(address)[0].coordinates
        except:
            LAT = globalsettings.google_map_lat
            LON = globalsettings.google_map_lon
    return (LAT, LON, ZOOM)


def com_rew_delete(sender, instance, **kwargs):
    try:
        modules = ['article','event','photoalbum','videos','movies','entry','classifieds','deal','business','attraction','banneradvertisements']
        if not sender.__name__.lower() in modules:
            return
        
        from mptt_comments.models import MpttComment
        from django.shortcuts import get_object_or_404
        key = {}
        model_name = sender.__name__.lower()
        try:c_type = get_object_or_404(ContentType,model=model_name)
        except:
            c_type=None
        key['content_type']=c_type
        key['object_pk']=instance.id
        comments=MpttComment.objects.prefetch_related('user').select_related('parent','parent__user').filter(**key)
        comments.delete()
    except:
        pass

pre_delete.connect(com_rew_delete)                  
                

comments_obj = CommonConfigure.objects.all()[:1][0]

DISQUS_SECRET_KEY = 'SbH4eT1LNCOmn4ZrszV4wE1asC2sg4YFDN6W1U17oHEEBsbOF5QdvfTslwGNMAsQ'
DISQUS_PUBLIC_KEY = 'Act5HOycthZRGcTa8V1ZeJJnUXVR7MyUGNv6G7eTfhmcL3jCGcXB4rpXXl2Qjx1J'

def get_disqus_sso(user_id, username, email):
    if user_id:
        user_data = {
            'id': user_id,
            'username': username,
            'email': email,
        }
    else:
        user_data = {}
    # create a JSON packet of our data attributes
    data = simplejson.dumps(user_data)
    # encode the data to base64
    message = base64.b64encode(data)
    # generate a timestamp for signing the message
    timestamp = int(time.time())
    # generate our hmac signature
    sig = hmac.HMAC(DISQUS_SECRET_KEY,'%s %s' % (message, timestamp), hashlib.sha1).hexdigest()

# return a script tag to insert the sso message
    return """<script type="text/javascript">
        var disqus_config = function() {
            this.page.remote_auth_s3 = "%(message)s %(sig)s %(timestamp)s";
            this.page.api_key = "%(pub_key)s";
            this.sso = {
                name:   "Blackmonk",
                button:  "%(siteurl)s/site_media/sitelogo/32d5477a-b883-49f9-8eb2-540bff7e0b28.png",
                url:     "%(siteurl)s/account/signin/",
                logout:  "%(siteurl)s/account/signout/",
                width:   "400",
                height:  "200",
            };
        }
    </script>""" % dict(
        siteurl = get_global_settings().website_url,
        message=message,
        timestamp=timestamp,
        sig=sig,
        pub_key=DISQUS_PUBLIC_KEY,
    )
    
def contactemail_save(request,classifieds):
    try:
        cont_obj = ContactEmails(content_object = classifieds)
        cont_obj.name = request.POST['respond_name']
        cont_obj.email = request.POST['respond_email']
        cont_obj.phone_no = request.POST['respond_phone']
        cont_obj.subject = classifieds.title
        cont_obj.message = request.POST['respond_msg']
        cont_obj.status = 'NR'
        cont_obj.created_by = request.user
        cont_obj.save()
    except:
        pass

from common.models import CoverPhoto

def getCoverPhoto(cobj):
    ctype = ContentType.objects.get_for_model(cobj)
    try:
        CoverObject = CoverPhoto.objects.get(content_type=ctype, object_id=cobj.id)
    except:
        CoverObject = False
    return CoverObject