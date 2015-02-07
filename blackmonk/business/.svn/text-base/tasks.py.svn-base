import celery
import csv
import datetime
from django.utils import timezone
from django.conf import settings as my_settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.mail import EmailMessage
from django.template import Template,Context
from django.template.defaultfilters import slugify
import urllib2

from business.models import Business, BusinessPrice, BusinessLogo, \
    BusinessCategory, PaymentOptions, Tag, WorkingHours, BusinessClaim
from common.getunique import getUniqueValue
from common.models import Address
from common.utils import date_fun, get_map_lat_lng_zoom, get_global_settings
from haystack.tasks import celery_rebuild_index
from usermgmt.models import EmailTemplates


# Variables used for CSV
BIZ_CSV_HEADER = ("NAME","LOGO","PARENT_CATEGORY","CATEGORIES","DESCRIPTION","SEO_TITLE","SEO_DESCRIPTION","STATUS","LISTING_TYPE","LISTING_PRICE","LISTING_START_DATE","LISTING_END_DATE","PAYMENT_PERIOD","IS_PAID","FACEBOOK_URL","TWITTER_URL","GOOGLEPLUS_URL","CAN_CLAIM","PAYMENT_OPTIONS","TAGS","ADDRESS1","ADDRESS2","PIN","CITY","TELEPHONE","MOBILENO","EMAIL","WEBSITE","LATITUDE","LONGITUDE","ZOOM","DISPLAY_OPERATION_HOURS","WORKING_HOUR_NOTES","MONDAY_START_TIME","MONDAY_CLOSING_TIME","TUESDAY_START_TIME","TUESDAY_CLOSING_TIME","WEDNESDAY_START_TIME","WEDNESDAY_CLOSING_TIME","THURSDAY_START_TIME","THURSDAY_CLOSING_TIME","FRIDAY_START_TIME","FRIDAY_CLOSING_TIME","SATURDAY_START_TIME","SATURDAY_CLOSING_TIME","SUNDAY_START_TIME","SUNDAY_CLOSING_TIME")
LISTING_TYPE_KEY = {'FEATURED':'F','SPONSORED':'S','FREE':'B'}
BIZ_STATUSES = ('PUBLISHED', 'PENDING', 'REJECTED', 'BLOCKED', 'DRAFTED')
BIZ_STATUS_KEY = {'PUBLISHED':'P','PENDING':'N','REJECTED':'R','BLOCKED':'B','DRAFTED':'D'}
ACCEPTED_TIME_FORMATS = (
    '%I:%M:%S %p',
    '%I:%M %p',
    '%H:%M'
)
ACCEPTED_DATE_FORMATS = (
    '%m/%d/%y %I:%M %p',
    '%m/%d/%y',
    '%m/%d/%Y',
    '%Y-%m-%d %H:%M:%S',
    '%Y/%m/%d %H:%M:%S',
    '%Y-%m-%d'
)

def mail_to_unpaid_user(user):
    global_settings = get_global_settings()
    to_emailid = [user.useremail, ]
    email_temp = EmailTemplates.objects.get(code='pcn')
    s = Template(email_temp.subject)
    sub = Context({"USERNAME": user.display_name,"WEBSITE": global_settings.domain})
    subject = s.render(sub)
    t= Template(email_temp.template)
    c= Context({"USERNAME": user.display_name,"WEBSITE": global_settings.domain})
    email_message=t.render(c)
    email= EmailMessage(subject,email_message,my_settings.DEFAULT_FROM_EMAIL,to_emailid)
    email.content_subtype = "html"
    email.send()

@celery.task(name='tasks.process_unpaid_business')
def process_unpaid_business():
    today = timezone.now()
    unpaid_claims = BusinessClaim.objects.filter(is_paid=False, claimed_on__lt=today)
    for claim in unpaid_claims:
        duration = today.date() - claim.claimed_on.date()
        if duration.days >= 1:
            mail_to_unpaid_user(claim.user)
            buz = claim.business
            buz.is_claimable = True
            buz.is_paid = False
            buz.status = 'P'
            buz.save()
            claim.delete()
    unpaid_userbiz = Business.objects.filter(
        is_paid=False, 
        created_on__lt=today,
        created_by__is_staff=False,
    ).exclude(
        featured_sponsored='B',
        status='D'
    )
    for buz in unpaid_userbiz:
        duration = today.date() - buz.created_on.date()
        if duration.days >= 1:
            mail_to_unpaid_user(buz.created_by)
            buz.status = 'D'
            buz.save()

    return "SUCCESS"

@celery.task(name='tasks.process_business_expires')
def process_business_expires():
    business = Business.objects.filter(status='P', lend_date__lt=date_fun()['three_days_after']).exclude(featured_sponsored='B')
    business.update(featured_sponsored='B')
    business.update(payment=BusinessPrice.objects.get(level='level0'))
    return "Success"


def clean_time_format(timestr):
    rtnstr = ''
    for tfmt in ACCEPTED_TIME_FORMATS:
        try:
            rtnstr = datetime.datetime.strptime(timestr, tfmt).strftime('%I:%M %p')
            break
        except:
            continue
    return rtnstr


def validate_and_clean(row, rownum):
    valid, msg, cleandata, invalidcols = True, "\nRow %d: %s" % (rownum, row['NAME'].strip()), dict(), set()
    for key in row: row[key] = row[key].strip().decode("utf-8")
    cleandata.update(row)
    # --------------------------------------------------------------------------
    catlist = []
    if row['PARENT_CATEGORY'] and row['CATEGORIES']:
        try:
            cleandata['PARENT_CATEGORY'] = BusinessCategory.objects.get(name=row['PARENT_CATEGORY'], parent_cat=None)
            for cat in row['CATEGORIES'].split(","):
                cat = cat.strip()
                if cat:
                    try:
                        category = BusinessCategory.objects.get(name=cat, parent_cat=cleandata['PARENT_CATEGORY'])
                        catlist.append(category)
                    except:
                        pass
        except:
            pass
    if not catlist:
        try:
            default_cat = BusinessCategory.objects.get(name='Uncategorized', parent_cat__name='Uncategorized')
        except:
            uc_parent = BusinessCategory.objects.get_or_create(
                name='Uncategorized',
                slug='uncategorized_parent',
                parent_cat=None
            )[0]
            default_cat = BusinessCategory.objects.get_or_create(
                name='Uncategorized',
                slug='uncategorized_sub',
                parent_cat=uc_parent
            )[0]
        catlist.append(default_cat)
        msg += "\n\tWarning: One or more CATEGORIES not matching with any of the Existing Categories. So, this will be listed under 'Uncategorized'"
    cleandata['CATEGORIES'] = catlist
    # --------------------------------------------------------------------------
    for field in ('NAME', 'CITY', 'DESCRIPTION', 'ADDRESS1'):
        if not row[field]:
            valid = False
            invalidcols.add(field)
            msg += "\n\t%s cannot be empty" % (field)
    # --------------------------------------------------------------------------
    cleandata['LISTING_TYPE'] = LISTING_TYPE_KEY[row['LISTING_TYPE']] if row['LISTING_TYPE'] in LISTING_TYPE_KEY else "B"
    datecheck = True
    for field in ('LISTING_START_DATE', 'LISTING_END_DATE'):
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
        if cleandata['LISTING_END_DATE'].date() < cleandata['LISTING_START_DATE'].date():
            valid = False
            invalidcols.add('LISTING_END_DATE')
            msg += "\n\tLISTING_END_DATE date should be greater than LISTING_START_DATE"
#     if cleandata['LISTING_TYPE'] in ('F', 'S'):
#     else:
#         cleandata['LISTING_START_DATE'] = cleandata['LISTING_END_DATE'] = None
    # --------------------------------------------------------------------------
    if row['STATUS'].upper() not in BIZ_STATUSES:
        valid = False
        invalidcols.add('STATUS')
        msg += "\n\tSTATUS not matching with " + str(BIZ_STATUSES)
    else:
        cleandata['STATUS'] = BIZ_STATUS_KEY[row['STATUS'].upper()]
    # --------------------------------------------------------------------------
    cleandata['NAME'] = row['NAME'][:120]
    if valid:
        cleandata['SLUG'] = getUniqueValue(Business, slugify(cleandata['NAME']))
        cleandata['LISTING_PRICE'] = float(row['LISTING_PRICE']) if row['LISTING_PRICE'].replace(".", "").isdigit() else 0.0
        # --------------------------------------------------------------------------
        for field in ['FACEBOOK_URL', 'TWITTER_URL', 'GOOGLEPLUS_URL']:
            if row[field] and 'http:' not in row[field]:
                cleandata[field] = "http://" + row[field]
        if row['PAYMENT_OPTIONS']:
            paymentoptlist = []
            for po in row['PAYMENT_OPTIONS'].split(','):
                try: paymentoptlist.append(PaymentOptions.objects.get(name__iexact = po.strip()))
                except: pass
            cleandata['PAYMENT_OPTIONS'] = paymentoptlist
        else:
            cleandata['PAYMENT_OPTIONS'] = []
        # --------------------------------------------------------------------------
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
        # --------------------------------------------------------------------------
        cleandata['PAYMENT_PERIOD'] = {"YEARLY": "Y", "MONTHLY": "M"}.get(row['PAYMENT_PERIOD'])
        # --------------------------------------------------------------------------
        cleandata['SEO_DESCRIPTION'] = row['SEO_DESCRIPTION'][:160] if row['SEO_DESCRIPTION'] else row['DESCRIPTION'][:160]
        # --------------------------------------------------------------------------
        cleandata['SEO_TITLE'] = row['SEO_TITLE'][:70] if row['SEO_TITLE'] else row['NAME'][:70]
        # --------------------------------------------------------------------------
        for field in ('CAN_CLAIM', 'IS_PAID', 'DISPLAY_OPERATION_HOURS'):
            cleandata[field] = row[field].upper() == "TRUE"
        # --------------------------------------------------------------------------
        if cleandata['DISPLAY_OPERATION_HOURS']:
            for timeentry in ("MONDAY_START_TIME","MONDAY_CLOSING_TIME","TUESDAY_START_TIME","TUESDAY_CLOSING_TIME","WEDNESDAY_START_TIME","WEDNESDAY_CLOSING_TIME","THURSDAY_START_TIME","THURSDAY_CLOSING_TIME","FRIDAY_START_TIME","FRIDAY_CLOSING_TIME","SATURDAY_START_TIME","SATURDAY_CLOSING_TIME","SUNDAY_START_TIME","SUNDAY_CLOSING_TIME"):
                cleandata[timeentry] = clean_time_format(row[timeentry])
            cleandata['WORKINGHOUR'] = WorkingHours(
                notes     = cleandata['WORKING_HOUR_NOTES'],    status  = 'P',
                mon_start = cleandata['MONDAY_START_TIME'],     mon_end = cleandata['MONDAY_CLOSING_TIME'],
                tue_start = cleandata['TUESDAY_START_TIME'],    tue_end = cleandata['TUESDAY_CLOSING_TIME'],
                wed_start = cleandata['WEDNESDAY_START_TIME'],  wed_end = cleandata['WEDNESDAY_CLOSING_TIME'],
                thu_start = cleandata['THURSDAY_START_TIME'],   thu_end = cleandata['THURSDAY_CLOSING_TIME'],
                fri_start = cleandata['FRIDAY_START_TIME'],     fri_end = cleandata['FRIDAY_CLOSING_TIME'],
                sat_start = cleandata['SATURDAY_START_TIME'],   sat_end = cleandata['SATURDAY_CLOSING_TIME'],
                sun_start = cleandata['SUNDAY_START_TIME'],     sun_end = cleandata['SUNDAY_CLOSING_TIME'],
            )
            cleandata['WORKINGHOUR'].save()
        else:
            cleandata['WORKINGHOUR'] = None
        cleandata['BUSINESSPRICE'] = BusinessPrice.objects.get(level={'B': 'level0', 'S': 'level1', 'F': 'level2'}[cleandata['LISTING_TYPE']])
        cleandata['LATITUDE'], cleandata['LONGITUDE'], cleandata['ZOOM'] = get_map_lat_lng_zoom(
            row['LATITUDE'], row['LONGITUDE'], row['ZOOM'],
            row['ADDRESS1'], row['ADDRESS2'], row['PIN'], row['CITY']
        )
    return {"msg": msg, "valid": valid, "cleandata": cleandata,
        "invalidcols": invalidcols}


@celery.task(name='tasks.process_business_csv_upload')
def process_business_csv_upload(csvfile):
    rownum, added, msg, invalidcols, user = 0, 0, "", set(), csvfile.uploaded_by
    rows = csv.DictReader(csvfile.file)
    if str(type(csvfile)) != "<class '__main__.UploadViaCron'>":
        csvfile.status = 'P'
        csvfile.save()
    for row in rows:
        if not set(row.keys()) == set(BIZ_CSV_HEADER):
            break
        rownum += 1
        cleandata = validate_and_clean(row, rownum)
        if not cleandata['valid']:
            msg += cleandata['msg'] + "\n"
            invalidcols.update(cleandata['invalidcols'])
        else:
            NewObj = Business(name=cleandata['cleandata']['NAME'],
            slug=cleandata['cleandata']['SLUG'],
            operating_hours=cleandata['cleandata']['DISPLAY_OPERATION_HOURS'],
            workinghours=cleandata['cleandata']['WORKINGHOUR'],
            summary=cleandata['cleandata']['DESCRIPTION'][:600],
            description=cleandata['cleandata']['DESCRIPTION'],
            seo_title=cleandata['cleandata']['SEO_TITLE'],
            seo_description=cleandata['cleandata']['SEO_DESCRIPTION'],
            featured_sponsored=cleandata['cleandata']['LISTING_TYPE'],
            sp_cost=cleandata['cleandata']['LISTING_PRICE'],
            lstart_date=cleandata['cleandata']['LISTING_START_DATE'],
            lend_date=cleandata['cleandata']['LISTING_END_DATE'],
            payment=cleandata['cleandata']['BUSINESSPRICE'],
            payment_type=cleandata['cleandata']['PAYMENT_PERIOD'],
            is_paid=cleandata['cleandata']['IS_PAID'],
            fb_url=cleandata['cleandata']['FACEBOOK_URL'],
            twitter_url=cleandata['cleandata']['TWITTER_URL'],
            gooleplus_url=cleandata['cleandata']['GOOGLEPLUS_URL'],
            is_claimable=cleandata['cleandata']['CAN_CLAIM'],
            status=cleandata['cleandata']['STATUS'],
            album=None, created_by=user, modified_by=user)
            if cleandata['cleandata']['LOGO']:
                try:
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(
                        urllib2.urlopen(cleandata['cleandata']['LOGO']).read()
                    )
                    img_temp.flush()
                    logo = BusinessLogo()
                    logo.uploaded_by = user
                    logo.logo.save(NewObj.slug + '.jpg', File(img_temp))
                    logo.save()
                    NewObj.logo = logo
                except:
                    pass
            NewObj.save()
            # Following are M2M fields
            ADDRESS = Address(
                venue=cleandata['cleandata']['NAME'],
                address_type="business",
                slug=cleandata['cleandata']['SLUG'],
                address1=cleandata['cleandata']['ADDRESS1'][:200],
                address2=cleandata['cleandata']['ADDRESS2'][:200],
                city=cleandata['cleandata']['CITY'][:100],
                telephone1=cleandata['cleandata']['TELEPHONE'][:20],
                mobile=cleandata['cleandata']['MOBILENO'][:20],
                email=cleandata['cleandata']['EMAIL'][:75],
                website=cleandata['cleandata']['WEBSITE'][:250],
                zip=cleandata['cleandata']['PIN'][:16],
                lat=cleandata['cleandata']['LATITUDE'],
                lon=cleandata['cleandata']['LONGITUDE'],
                zoom=cleandata['cleandata']['ZOOM'],
                seo_title=cleandata['cleandata']['SEO_TITLE'][:70],
                seo_description=cleandata['cleandata']['SEO_DESCRIPTION'][:160],
                type=None, state="", country="", description="", telephone2="",
                fax="", status='P', created_by=user, modified_by=user
            )
            ADDRESS.save()
            NewObj.address.add(ADDRESS)
            for cat in cleandata['cleandata']['CATEGORIES']:
                NewObj.categories.add(cat)
            for payopt in cleandata['cleandata']['PAYMENT_OPTIONS']:
                NewObj.paymentoptions.add(payopt)
            for tag in cleandata['cleandata']['TAGS']:
                NewObj.tags.add(tag)
            NewObj.save()
            added += 1
    if added == rownum:
        status = 'S'
        log = emailalert = "%d Business has been added.\n\n" % (rownum)
    else:
        status = 'E'
        log = emailalert = "%d Out of %d Business has been added.\n\n" % \
            (added, rownum)
    if invalidcols:
        log += "The Columns " + str(tuple(invalidcols)) + \
            " are having errors,\n\n"
    if not added:
        status = 'E'
    log += msg
    if str(type(csvfile)) != "<class '__main__.UploadViaCron'>":
        csvfile.status = status
        csvfile.log = log
        csvfile.save()
        try:
            emailalert = "<pre>" + emailalert + "</pre><br><a href='" + \
                csvfile.get_log_url() + "'>Click here for more details</a>"
            email = EmailMessage('Business Adding via CSV', emailalert,
                my_settings.DEFAULT_FROM_EMAIL, [user.useremail])
            email.content_subtype = "html"
            email.send()
        except:
            pass
        if added:
            try:
                celery_rebuild_index.delay()
            except:
                pass
        return "Success"
    else:
        return log