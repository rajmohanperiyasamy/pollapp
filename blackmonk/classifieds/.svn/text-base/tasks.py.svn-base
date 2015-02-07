import celery
import csv
import datetime
from django.conf import settings as my_settings
from django.core.mail.message import EmailMessage
from django.template.defaultfilters import slugify

from classifieds.models import Classifieds, ClassifiedCategory, Tag, \
    ClassifiedPrice
from common.getunique import getUniqueValue
from common.models import Address
from common.utils import date_fun, get_map_lat_lng_zoom
from haystack.tasks import celery_rebuild_index


@celery.task(name='tasks.process_classifieds_expires')
def process_classifieds_expires():
    Classifieds.objects.filter(status='P', listing_end_date__lt=date_fun()['today']).update(status='E', listing_type='B', is_paid=False)
    return "Success"

CLASSIFIED_CSV_HEADER = ('TITLE','DESCRIPTION','PARENT_CATEGORY','SUB_CATEGORY','STATUS','AD_TYPE','TAGS','CLASSIFIED_PRICE','LISTING_TYPE','LISTING_PRICE','LISTING_START_DATE','LISTING_END_DATE','LISTING_IS_PAID','SEO_TITLE','SEO_DESCRIPTION','ADDRESS1','ADDRESS2','PIN','CITY','TELEPHONE','MOBILENO','EMAIL','WEBSITE','LATITUDE','LONGITUDE','ZOOM')
ADD_TYPES = ('SELL','BUY','RENT','RENTOUT')
ADD_TYPE_KEY = {'SELL':'S','BUY':'B','RENT':'R','RENTOUT':'O'}
LISTINGTYPES = ('FEATURED','SPONSORED','FREE')
LISTINGTYPE_KEY = {'FEATURED':'F','SPONSORED':'S','FREE':'B'}
STATUS_KEY = {'PUBLISHED':'P','PENDING':'N','EXPIRED':'E','REJECTED':'R','BLOCKED':'B','DRAFTED':'D'}
STATUSES = ('PUBLISHED','PENDING','EXPIRED','REJECTED','BLOCKED','DRAFTED')
ACCEPTED_DATE_FORMATS = (
    '%m/%d/%y %I:%M %p',
    '%Y-%m-%d %H:%M:%S', 
    '%Y/%m/%d %H:%M:%S',
    '%d/%m/%y %H:%M:%S',
    '%d-%m-%y %H:%M:%S',
    '%d/%m/%y %H:%M',
    '%d-%m-%y %H:%M',
    '%m/%d/%y',
    '%m/%d/%Y',
    '%Y-%m-%d'
)

def validate_and_clean(row, rownum):
    valid, msg, cleandata, invalidcols = True, "Row %d:" % (rownum), dict(), set()
    for key in row:
        row[key] = row[key].strip().decode("utf-8")
    cleandata.update(row)
    # ----------------------------Mandatory Fields-------------------------------
    for field in ('DESCRIPTION','PIN', 'CITY', 'EMAIL'):
        if not row[field]:
            valid = False
            invalidcols.add(field)
            msg += "\n\t%s cannot be empty" % (field)
    # --------------------------------------------------------------------------
    if not row['PARENT_CATEGORY'] or not row['SUB_CATEGORY']:
        category = ClassifiedCategory.objects.get(name__iexact='Uncategorized',parent__name__iexact='Uncategorized')
        cleandata['CATEGORY'] = category
        msg += "\n\tPARENT_CATEGORY or SUB_CATEGORY is Empty. So, by default category is set to Uncategorized"
    else:
        try:
            category = ClassifiedCategory.objects.get(name__iexact=row['PARENT_CATEGORY'])
            cat = ClassifiedCategory.objects.get(name__iexact=row['SUB_CATEGORY'],parent__name__iexact=row['PARENT_CATEGORY'])
            cleandata['CATEGORY'] = cat
        except:
            category = ClassifiedCategory.objects.get(name__iexact='Uncategorized',parent__name__iexact='Uncategorized')
            cleandata['CATEGORY'] = category
            msg += "\n\tPARENT CATEGORY or SUB_CATEGORY not matching with any of the Existing Category. So, by default category is set to Uncategorized"
            pass
 
    # --------------------------------------------------------------------------
    if row['STATUS'].upper() not in STATUSES:
        valid = False
        invalidcols.add('STATUS')
        msg += "\n\tSTATUS not matching with " + str(STATUSES)
    else:
        cleandata['STATUS'] = STATUS_KEY[row['STATUS'].upper()]
    # --------------------------------------------------------------------------
    if not row['ADDRESS1']:
        valid = False
        invalidcols.add('ADDRESS1')
        msg += "\n\tADDRESS1 cannot be Empty"
    else:
        cleandata['LATITUDE'],cleandata['LONGITUDE'],cleandata['ZOOM']= get_map_lat_lng_zoom(
                row['ADDRESS1'], row['ADDRESS2'], row['CITY'], row['PIN'], row['LATITUDE'],row['LONGITUDE'],row['ZOOM']
                )
    # --------------------------------------------------------------------------
    if not row['TITLE']:
        valid = False
        invalidcols.add('TITLE')
        msg += "\n\tTITLE cannot be Empty"
    else:
        cleandata['TITLE'] = row['TITLE'][:200]
        if valid:
            cleandata['SLUG'] = getUniqueValue(Classifieds, slugify(cleandata['TITLE']))
    # --------------------------------------------------------------------------
    if row['TAGS'] and valid:
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
    else:
        cleandata['TAGS'] = []
    # --------------------------------------------------------------------------
    cleandata['LISTING_TYPE'] = LISTINGTYPE_KEY[row['LISTING_TYPE'].upper()] if row['LISTING_TYPE'].upper() in LISTINGTYPES else "B"
    # --------------------------------------------------------------------------
    if cleandata['LISTING_TYPE'] in ('S', 'F'): 
        datecheck = True
        if row['LISTING_START_DATE'] and row['LISTING_END_DATE']:
            for dformat in ACCEPTED_DATE_FORMATS:
                try:
                    cleandata['LISTING_START_DATE'] = datetime.datetime.strptime(row['LISTING_START_DATE'], dformat)
                    break
                except:
                    continue
            else:
                valid = datecheck = False
                invalidcols.add('LISTING_START_DATE')
                msg += "\n\tLISTING_START_DATE date format is not wrong"
            for dformat in ACCEPTED_DATE_FORMATS:
                try:
                    cleandata['LISTING_END_DATE'] = datetime.datetime.strptime(row['LISTING_END_DATE'], dformat)
                    break
                except:
                    continue
            else:
                valid = datecheck = False
                invalidcols.add('LISTING_END_DATE')
                msg += "\n\tLISTING_END_DATE format is not correct"
            if datecheck:
                if not cleandata['LISTING_START_DATE'].date() < cleandata['LISTING_END_DATE'].date():
                    valid = False
                    msg += "\n\tError! LISTING_START_DATE not greater than LISTING_END_DATE" 
    else:
        cleandata['LISTING_START_DATE'] = None
        cleandata['LISTING_END_DATE'] = None
    
    # --------------------------Optional Fields------------------------------------------------
    if valid:
        cleandata['AD_TYPE'] = ADD_TYPE_KEY[row['AD_TYPE'].upper()] if row['AD_TYPE'].upper() in ADD_TYPES else "B"
        # --------------------------------------------------------------------------
        if not row['CLASSIFIED_PRICE']:cleandata['CLASSIFIED_PRICE'] = 0.0
        # --------------------------------------------------------------------------
        try:cleandata['PAYMENT'] = ClassifiedPrice.objects.get(level={'F':'level2','S':'level1','B':'level0'}[cleandata['LISTING_TYPE']])
        except:cleandata['PAYMENT'] = ClassifiedPrice.objects.get(level='level0')
        # --------------------------------------------------------------------------
        cleandata['LISTING_IS_PAID'] = row['LISTING_IS_PAID'].upper() == 'TRUE'
        # --------------------------------------------------------------------------
        if row['SEO_TITLE']:cleandata['SEO_TITLE'] = row['SEO_TITLE'][:70]
        else:cleandata['SEO_TITLE'] = row['TITLE'][:70]
        # --------------------------------------------------------------------------
        if row['SEO_DESCRIPTION']:cleandata['SEO_DESCRIPTION'] = row['SEO_DESCRIPTION'][:160]
        else:cleandata['SEO_DESCRIPTION'] = row['DESCRIPTION'][:160]
        # -------------------------------------------------------------------------- 
    
    return {"msg": msg, "valid": valid, "cleandata": cleandata, "invalidcols": invalidcols}


@celery.task(name='tasks.process_classifieds_csv_upload')
def process_classifieds_csv_upload(csvfile):
    rownum, added, msg, invalidcols, user = 0, 0, "", set(), csvfile.uploaded_by
    rows = csv.DictReader(csvfile.file)
    csvfile.status = 'P'
    csvfile.save()
    for row in rows:
        if not set(row.keys()) == set(CLASSIFIED_CSV_HEADER):
            break
        rownum += 1
        cleandata = validate_and_clean(row, rownum)
        if not cleandata['valid']:
            msg += cleandata['msg'] + "\n"
            invalidcols.update(cleandata['invalidcols'])
        else:
            newobject = Classifieds()
            newobject.title = cleandata["cleandata"]['TITLE']
            newobject.description = cleandata["cleandata"]['DESCRIPTION']
            newobject.category = cleandata["cleandata"]['CATEGORY']
            newobject.action = cleandata["cleandata"]['AD_TYPE']
            newobject.slug = cleandata["cleandata"]['SLUG']
            newobject.status = cleandata["cleandata"]['STATUS']
            newobject.classified_price = cleandata["cleandata"]['CLASSIFIED_PRICE']
            newobject.payment= cleandata["cleandata"]['PAYMENT']
            newobject.listing_type = cleandata["cleandata"]['LISTING_TYPE']
            newobject.price = cleandata["cleandata"]['LISTING_PRICE']
            newobject.listing_start_date = cleandata["cleandata"]['LISTING_START_DATE']
            newobject.listing_end_date = cleandata["cleandata"]['LISTING_END_DATE']
            newobject.is_paid = cleandata["cleandata"]['LISTING_IS_PAID']
            newobject.seo_title = cleandata["cleandata"]['SEO_TITLE']
            newobject.seo_description = cleandata["cleandata"]['SEO_DESCRIPTION']
            
            address = Address()
            address.venue = cleandata["cleandata"]['TITLE']
            address.type = None
            address.status = 'P'
            address.address1 = cleandata["cleandata"]['ADDRESS1']
            address.address2 = cleandata["cleandata"]['ADDRESS2']
            address.zip = cleandata["cleandata"]['PIN']
            address.city = cleandata["cleandata"]['CITY']
            address.telephone1 = cleandata["cleandata"]['TELEPHONE']
            address.mobile = cleandata["cleandata"]['MOBILENO']
            address.email = cleandata["cleandata"]['EMAIL']
            address.website = cleandata["cleandata"]['WEBSITE'] if cleandata["cleandata"]['WEBSITE'] and len(cleandata["cleandata"]['WEBSITE']) < 200 else ""
            address.lat = cleandata["cleandata"]['LATITUDE']
            address.lon = cleandata["cleandata"]['LONGITUDE']
            address.zoom = cleandata["cleandata"]['ZOOM']
            address.created_by = user
            address.modified_by = user
            address.address_type = "classified"
            address.save()
            newobject.address = address
            
            newobject.published_on = datetime.datetime.today()
            newobject.created_on = datetime.datetime.today()
            newobject.created_by = newobject.modified_by = user
            newobject.save()
            
            for tag in cleandata["cleandata"]['TAGS']:
                newobject.tags.add(tag)
            added += 1
    if added == rownum:
        csvfile.status = 'S'
        csvfile.log = emailalert = "%d Classifieds have been added successfully.\n\n" % (rownum)
    else:
        csvfile.status = 'E'
        csvfile.log = emailalert = "%d Out of %d Classifieds have been added.\n\n" % (added, rownum)
    if invalidcols: csvfile.log += "The Columns " + str(tuple(invalidcols)) + " are having errors,\n\n"
    if not added: csvfile.status = 'E'
    csvfile.log += msg
    csvfile.save() 
    try:
        emailalert = "<pre>"+emailalert+"</pre><br><a href='"+csvfile.get_log_url()+"'>Click here for more details</a>"
        email = EmailMessage('Classifieds Adding via CSV', emailalert, my_settings.DEFAULT_FROM_EMAIL, [user.useremail])
        email.content_subtype = "html"
        email.send()
    except:
        pass
    if added:
        try: celery_rebuild_index.delay()
        except: pass
    return "Success"