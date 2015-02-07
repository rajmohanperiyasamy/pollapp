import celery
import csv
import datetime
from django.conf import settings as my_settings
from django.core.mail import EmailMessage
from django.template.defaultfilters import slugify

from common.getunique import getUniqueValue
from common.models import Address, VenueType
from common.utils import date_fun, get_map_lat_lng_zoom, ds_cleantext
from events.models import Event, EventPrice, EventCategory, Tag, EventOccurence
from haystack.tasks import celery_rebuild_index


LISTING_TYPE_KEY = {'FEATURED':'F','SPONSORED':'S','FREE':'B'}
EVNT_STATUS_KEY = {'PUBLISHED':'P','PENDING':'N','REJECTED':'R','BLOCKED':'B','DRAFTED':'D','EXPIRED':'E'}
EVNT_STATUSES = ('PUBLISHED', 'PENDING', 'REJECTED', 'BLOCKED', 'DRAFTED', 'EXPIRED')
EVNT_CSV_HEADER = ("TITLE","EVENT_DESCRIPTION","CATEGORY","STATUS","START_DATE","END_DATE","START_TIME","END_TIME","TICKET_PRIZE","TICKET_WEBSITE","TICKET_PHONE_NO","EVENT_WEBSITE","FACEBOOK","GOOGLEPLUS","CONTACT_EMAIL","PHONE","LISTING_TYPE","LISTING_PRICE","LISTING_START","LISTING_END","IS_PAID","SEO_TITLE","SEO_DESCRIPTION","TAGS","VENUE_NAME","VENUE_ADDRESS1","VENUE_ADDRESS2","VENUE_TYPE","VENUE_PHONE_NO","VENUE_MOBILE_NO","VENUE_EMAIL","VENUE_WEBSITE_URL","VENUE_DESCRIPTION","VENUE_ZIPCODE","VENUE_LATITUDE","VENUE_LONGITUDE","VENUE_MAPZOOM","VENUE_SEO_TITLE","VENUE_SEO_DESCRIPTION")


def get_next_day(event,today):
    occ_objs = EventOccurence.objects.filter(event=event).order_by('id')
    for occ_obj in occ_objs:
        if occ_obj.date >= today:
            return occ_obj.date_

@celery.task(name='tasks.process_event_expires')
def process_event_expires():
    Event.objects.filter(status='P', end_date__lt=date_fun()['today']).update(status='E')
    events = Event.objects.filter(status='P', listing_end__lt=date_fun()['today']).exclude(listing_type='B')
    pay = EventPrice.objects.get(level='level0')
    events.update(listing_type='B', payment=pay)
    
    events_rcr = Event.objects.filter(status='P', is_reoccuring = True,start_date__lte = date_fun()['today'])
    for event in events_rcr:
        event.start_date = get_next_day(event,date_fun()['today'])
        event.save()
    return "Success"

ACCEPTED_TIME_FORMATS = (
    '%I:%M:%S %p',
    '%I:%M %p',
    '%H:%M'
)
def clean_time_format(timestr):
    rtntime = None
    for tfmt in ACCEPTED_TIME_FORMATS:
        try:
            rtntime = datetime.datetime.strptime(timestr, tfmt).time()
            break
        except:
            continue
    return rtntime
ACCEPTED_DATE_FORMATS = (
    '%Y-%m-%d',
    '%m/%d/%y %I:%M %p',
    '%m/%d/%y',
    '%m/%d/%Y',
    '%Y-%m-%d %H:%M:%S',
    '%Y/%m/%d %H:%M:%S',
)

def validate_and_clean(row, rownum):
    valid, msg, cleandata, invalidcols = True, "Row %d: %s" % (rownum, row['TITLE'].strip()), dict(), set()
    for key in row: row[key] = row[key].strip().decode("utf-8")
    cleandata.update(row)
    # --------------------------------------------------------------------------
    for field in ("TITLE", "EVENT_DESCRIPTION", "VENUE_NAME", "VENUE_TYPE", "VENUE_ADDRESS1", "VENUE_ZIPCODE"):
        if not row[field]:
            valid = False
            invalidcols.add(field)
            msg += "\n\t%s cannot be empty" % (field)
    # --------------------------------------------------------------------------
    catlist = []
    if not row["CATEGORY"]:
        catlist.append(EventCategory.objects.get(name='Uncategorized'))
        msg += "\n\tCATEGORY is empty. So, by default category is set to Uncategorized"
    else:
        for cat in row["CATEGORY"].split(","):
            cat = cat.strip()
            if valid and cat:
                try:
                    category = EventCategory.objects.get(name=cat)
                    catlist.append(category)
                except:
                    pass
        if not catlist:
            catlist.append(EventCategory.objects.get(name='Uncategorized'))
            msg += "\n\tOne or more CATEGORY not matching with any of the Existing Categories. So, by default category is set to Uncategorized"
    cleandata["CATEGORY"] = catlist
    # --------------------------------------------------------------------------
    if row["STATUS"] not in EVNT_STATUSES:
        valid = False
        invalidcols.add('STATUS')
        msg += "\n\tSTATUS not matching with " + str(EVNT_STATUSES)
    else:
        cleandata['STATUS'] = EVNT_STATUS_KEY[row['STATUS']]
    # --------------------------------------------------------------------------
    datecheck = True
    for field in ("START_DATE", "END_DATE"):
        for dformat in ACCEPTED_DATE_FORMATS:
            try:
                cleandata[field] = datetime.datetime.strptime(row[field], dformat).date()
                break
            except:
                continue
        else:
            valid = datecheck = False
            invalidcols.add(field)
            msg += "\n\t%s date format is wrong" % (field)
    if datecheck and cleandata['END_DATE'] < cleandata['START_DATE']:
        valid = False
        invalidcols.add('END_DATE')
        msg += "\n\tEND_DATE date should be less than or equal to START_DATE"
    # --------------------------------------------------------------------------
    if row["START_TIME"] and row ["END_TIME"]:
        for field in ("START_TIME","END_TIME"):
            cleandata[field] = clean_time_format(row[field])
    else:
        cleandata["START_TIME"] = cleandata["END_TIME"] = None
    # --------------------------------------------------------------------------
    cleandata["IS_PAID"] = row["IS_PAID"].upper() == "TRUE"
    # --------------------------------------------------------------------------
    cleandata['LISTING_TYPE'] = LISTING_TYPE_KEY[row['LISTING_TYPE']] if row['LISTING_TYPE'] in LISTING_TYPE_KEY else "B"
    if cleandata['LISTING_TYPE'] in ('F', 'S'):
        datecheck = True
        for field in ('LISTING_START', 'LISTING_END'):
            for dformat in ACCEPTED_DATE_FORMATS:
                try:
                    cleandata[field] = datetime.datetime.strptime(row[field], dformat)
                    break
                except:
                    continue
            else:
                valid = datecheck = False
                invalidcols.add(field)
                msg += "\n\t%s date format is wrong" % (field)
        if datecheck:
            if cleandata['LISTING_END'].date() < cleandata['LISTING_START'].date():
                valid = False
                invalidcols.add('LISTING_END')
                msg += "\n\tLISTING_END date should be greater than LISTING_START"
    else:
        cleandata['LISTING_START'] = cleandata['LISTING_END'] = None
    # --------------------------------------------------------------------------
    for field in ("LISTING_PRICE", "TICKET_PRIZE"):
        if not row[field].replace(".","").isdigit(): cleandata[field] = "0"
    # --------------------------------------------------------------------------
    if valid:
        cleandata['SLUG'] = getUniqueValue(Event, slugify(cleandata['TITLE']))
        if not row["SEO_TITLE"]: cleandata["SEO_TITLE"] = row["TITLE"][:70]
        if not row["SEO_DESCRIPTION"]: cleandata["SEO_DESCRIPTION"] = row["EVENT_DESCRIPTION"][:160]
        cleandata['VENUE_LATITUDE'], cleandata['VENUE_LONGITUDE'], cleandata['VENUE_MAPZOOM'] = get_map_lat_lng_zoom(row['VENUE_LATITUDE'],row['VENUE_LONGITUDE'],row['VENUE_MAPZOOM'], row['VENUE_ADDRESS1'], row['VENUE_ADDRESS2'], row['VENUE_ZIPCODE'], "")
        taglist = list()
        for tag in row['TAGS'].split(','):
            tag = tag.strip()
            if tag:
                try:
                    tagobj = Tag.objects.get(tag__iexact=tag)
                except:
                    tagobj = Tag(tag=tag)
                    tagobj.save()
                taglist.append(tagobj)
        cleandata['TAGS'] = taglist
        cleandata['VENUE_LATITUDE'], cleandata['VENUE_LONGITUDE'], cleandata['VENUE_MAPZOOM'] = get_map_lat_lng_zoom(
            row['VENUE_LATITUDE'], row['VENUE_LONGITUDE'], row['VENUE_MAPZOOM'],
            row['VENUE_ADDRESS1'], row['VENUE_ADDRESS2'], row['VENUE_ZIPCODE'], ""
        )
    # --------------------------------------------------------------------------
    return {"msg": msg, "valid": valid, "cleandata": cleandata, "invalidcols": invalidcols}

@celery.task(name='tasks.process_events_csv_upload')
def process_events_csv_upload(csvfile):
    rownum, added, msg, invalidcols, user = 0, 0, "", set(), csvfile.uploaded_by
    rows = csv.DictReader(csvfile.file)
    csvfile.status = 'P'
    csvfile.save()
    for row in rows:
        if not set(row.keys()) == set(EVNT_CSV_HEADER):
            break
        rownum += 1
        cleandata = validate_and_clean(row, rownum)
        if not cleandata['valid']:
            msg += cleandata['msg'] + "\n"
            invalidcols.update(cleandata['invalidcols'])
        else:
            try:
                venue=Address.objects.get(
                    venue__iexact = cleandata['cleandata']['VENUE_NAME'],
                    address1__iexact = cleandata['cleandata']['VENUE_ADDRESS1'],
                    zip__iexact = cleandata['cleandata']['VENUE_ZIPCODE']
                )
            except: 
                venue = Address()
                venue.venue         = cleandata['cleandata']['VENUE_NAME'] 
                venue.slug          = getUniqueValue(Address,slugify(cleandata['cleandata']['VENUE_NAME']))
                venue.address1      = cleandata['cleandata']['VENUE_ADDRESS1'][:200]
                venue.address2      = cleandata['cleandata']['VENUE_ADDRESS2'][:200] if row['VENUE_ADDRESS2'] else ""
                venue.telephone1    = cleandata['cleandata']['VENUE_PHONE_NO'][:20]
                venue.mobile        = cleandata['cleandata']['VENUE_MOBILE_NO'][:20]
                venue.email         = cleandata['cleandata']['VENUE_EMAIL'][:75]
                venue.website       = cleandata['cleandata']['VENUE_WEBSITE_URL'][:250]
                venue.description   = cleandata['cleandata']['VENUE_DESCRIPTION']
                venue.zip           = cleandata['cleandata']['VENUE_ZIPCODE']
                venue.lat           = cleandata['cleandata']['VENUE_LATITUDE']
                venue.lon           = cleandata['cleandata']['VENUE_LONGITUDE']
                venue.zoom          = cleandata['cleandata']['VENUE_MAPZOOM']
                venue.address_type  = "events"
                venue.created_by = venue.modified_by = user
                venue.seo_title = ds_cleantext(cleandata['cleandata']['VENUE_SEO_TITLE'][:70]) if cleandata['cleandata']['VENUE_SEO_TITLE'] else ""
                venue.seo_description = ds_cleantext(cleandata['cleandata']['VENUE_SEO_DESCRIPTION'][:160]) if cleandata['cleandata']['VENUE_SEO_DESCRIPTION'] else ""
                try: venue.type = VenueType.objects.get(title__iexact=cleandata['cleandata']['VENUE_TYPE'])
                except: pass
                venue.save()
            NewObj = Event(
                title               = cleandata['cleandata']['TITLE'],
                event_description   = cleandata['cleandata']['EVENT_DESCRIPTION'],
                slug                = cleandata['cleandata']['SLUG'],
                start_date          = cleandata['cleandata']['START_DATE'],
                end_date            = cleandata['cleandata']['END_DATE'],
                start_time          = cleandata['cleandata']['START_TIME'],
                end_time            = cleandata['cleandata']['END_TIME'],
                is_reoccuring       = False,
                tkt_prize           = cleandata['cleandata']['TICKET_PRIZE'],
                ticket_site         = cleandata['cleandata']['TICKET_WEBSITE'],
                tkt_phone           = cleandata['cleandata']['TICKET_PHONE_NO'],
                event_website       = cleandata['cleandata']['EVENT_WEBSITE'],
                facebook            = cleandata['cleandata']['FACEBOOK'],
                googleplus          = cleandata['cleandata']['GOOGLEPLUS'],
                contact_email       = cleandata['cleandata']['CONTACT_EMAIL'],
                phone               = cleandata['cleandata']['PHONE'],
                seo_title           = cleandata['cleandata']['SEO_TITLE'],
                seo_description     = cleandata['cleandata']['SEO_DESCRIPTION'],
                listing_type        = cleandata['cleandata']['LISTING_TYPE'],
                payment             = EventPrice.objects.get(level={'B': 'level0', 'S': 'level1', 'F': 'level2'}[cleandata['cleandata']['LISTING_TYPE']]),
                listing_start       = cleandata['cleandata']['LISTING_START'],
                listing_end         = cleandata['cleandata']['LISTING_END'],
                listing_price       = cleandata['cleandata']['LISTING_PRICE'],
                is_paid             = cleandata['cleandata']['IS_PAID'],
                status              = cleandata['cleandata']['STATUS'],
                venue               = venue,
                album = None, created_by = user, modified_by = user,
            )
            NewObj.save()
            for tag in cleandata['cleandata']['TAGS']: NewObj.tags.add(tag)
            for cat in cleandata['cleandata']['CATEGORY']: NewObj.category.add(cat)
            NewObj.save()
            added += 1
    if added == rownum:
        csvfile.status = 'S'
        csvfile.log = emailalert = "%d Events has been added successfully.\n\n" % (rownum)
    else:
        csvfile.status = 'E'
        csvfile.log = emailalert = "%d Out of %d Events has been added.\n\n" % (added, rownum)
    if invalidcols: csvfile.log += "The Columns " + str(tuple(invalidcols)) + " are having errors,\n\n"
    if not added: csvfile.status = 'E'
    csvfile.log += msg
    csvfile.save() 
    try:
        emailalert = "<pre>"+emailalert+"</pre><br><a href='"+csvfile.get_log_url()+"'>Click here for more details</a>"
        email = EmailMessage('Events Adding via CSV', emailalert, my_settings.DEFAULT_FROM_EMAIL, [user.useremail])
        email.content_subtype = "html"
        email.send()
    except:
        pass
    if added:
        try: celery_rebuild_index.delay()
        except: pass
    return "Success"