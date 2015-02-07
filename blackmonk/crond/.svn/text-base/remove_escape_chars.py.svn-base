import getsettings
from django.db import connection
from domains import *
from xml.sax.saxutils import unescape

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


from events.models import Event
from attraction.models import Attraction
from classifieds.models import Classifieds 
from article.models import Article
from bookmarks.models import Bookmark
from business.models import Business
from deal.models import Deal
from gallery.models import PhotoAlbum
from jobs.models import JobDetail
from movies.models import Movies,Theatres
from news.models import News
for domain_name  in SCHEMATA_DOMAINS:
    connection.set_schemata_domain(domain_name)
    for module in [Event, Attraction, Classifieds, Article, Bookmark, Business, Deal, PhotoAlbum, JobDetail, Movies, News]:
        print "clearing escape chars in [", str(module), "] . . . . .",
        try:
            for obj in module.objects.all():
                try:
                    obj.seo_description = unescape(obj.seo_description, escape_dict).strip()
                    obj.save()
                except: pass
                try:
                    obj.seo_title = unescape(obj.seo_title, escape_dict).strip()
                    obj.save()
                except: pass  
            print "Done !!"
        except:
            from sys import exc_info
            print exc_info()
            print " -- Not Done !!"
    
    print "clearing escape chars in [", str(Theatres), "] . . . . .",
    try:
        for obj in Theatres.objects.all():
            try: 
                obj.theatreseo_description = unescape(obj.theatreseo_description, escape_dict).strip()
                obj.save()
            except: pass
            try: 
                obj.theatreseo_title = unescape(obj.theatreseo_title, escape_dict).strip()
                obj.save()
            except: pass
        print "Done !!"
    except: 
        print " -- Not Done !!"