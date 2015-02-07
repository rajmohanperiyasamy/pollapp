import celery
import csv
import datetime
from django.conf import settings as my_settings
from django.core.mail.message import EmailMessage
from django.template.defaultfilters import slugify

from article.models import ArticleCategory, Article, Tag
from common.getunique import getUniqueValue
from haystack.tasks import celery_rebuild_index


ARTICLE_CSV_HEADER = ("TITLE","CATEGORY","ARTICLE_TYPE","STATUS","SUMMARY","DESCRIPTION","SEO_TITLE","SEO_DESCRIPTION","FEATURED","TAGS","PUBLISHED_ON")
ARTICLE_TYPES = ('OWNSTORY', 'PRESSRELEASE', 'ADVERTORIAL', 'REVIEWREQUEST')
ARTICLE_TYPE_KEY = {'OWNSTORY':'FR','PRESSRELEASE':'PR','ADVERTORIAL':'A','REVIEWREQUEST':'RR'}
ARTICLE_STATUSES = ('PUBLISHED', 'PENDING', 'REJECTED', 'BLOCKED', 'DRAFTED', 'SCHEDULED')
ARTICLE_STATUS_KEY = {'PUBLISHED':'P','PENDING':'N','SCHEDULED':'S','REJECTED':'R','BLOCKED':'B','DRAFTED':'D'}
ACCEPTED_DATE_FORMATS = (
    '%m/%d/%y %I:%M %p',
    '%m/%d/%y',
    '%m/%d/%Y',
    '%Y-%m-%d %H:%M:%S',
    '%Y/%m/%d %H:%M:%S',
    '%Y-%m-%d'
)


def validate_and_clean(row, rownum):
    valid, msg, cleandata, invalidcols = True, "Row %d: %s" % (rownum, row['TITLE']), dict(), set()
    for key in row:
        row[key] = row[key].strip().decode("utf-8")
    cleandata.update(row)
    # --------------------------------------------------------------------------
    if row['ARTICLE_TYPE'] not in ARTICLE_TYPES:
        cleandata['ARTICLE_TYPE'] = 'FR'
    else:
        cleandata['ARTICLE_TYPE'] = ARTICLE_TYPE_KEY[row['ARTICLE_TYPE']]
    # --------------------------------------------------------------------------
    if not row['CATEGORY']:
        category = ArticleCategory.objects.get(name='Uncategorized')
        cleandata['CATEGORY'] = category
        msg += "\n\tCATEGORY is Empty. So, by default category is set to Uncategorized"
    else:
        try:
            category = ArticleCategory.objects.get(name=row['CATEGORY'])
            cleandata['CATEGORY'] = category
        except:
            category = ArticleCategory.objects.get(name='Uncategorized')
            cleandata['CATEGORY'] = category
            msg += "\n\tCATEGORY not matching with any of the Existing Category. So, by default category is set to Uncategorized"
            pass
    # --------------------------------------------------------------------------
    if not row['DESCRIPTION']:
        valid = False
        invalidcols.add('DESCRIPTION')
        msg += "\n\tDESCRIPTION cannot be Empty"
    # --------------------------------------------------------------------------
    cleandata['FEATURED'] = row['FEATURED'].upper() == 'TRUE'
    # --------------------------------------------------------------------------
    if row['STATUS'] not in ARTICLE_STATUSES:
        valid = False
        invalidcols.add('STATUS')
        msg += "\n\tSTATUS not matching with " + str(ARTICLE_STATUSES)
    else:
        cleandata['STATUS'] = ARTICLE_STATUS_KEY[row['STATUS']]
    # --------------------------------------------------------------------------
    if cleandata['STATUS'] in ('P', 'S'):
        for dformat in ACCEPTED_DATE_FORMATS:
            try:
                cleandata['PUBLISHED_ON'] = datetime.datetime.strptime(row['PUBLISHED_ON'], dformat)
                break
            except:
                continue
        else:
            valid = False
            invalidcols.add('PUBLISHED_ON')
            msg += "\n\tPUBLISHED_ON date format is wrong"
        if cleandata['STATUS'] == 'P' and cleandata['PUBLISHED_ON'].date() > datetime.datetime.today().date():
            valid = False
            invalidcols.add('PUBLISHED_ON')
            msg += "\n\tPUBLISHED_ON date should be less than or equal to today for Published Article"
        elif cleandata['STATUS'] == 'S' and cleandata['PUBLISHED_ON'].date() <= datetime.datetime.today().date():
            valid = False
            invalidcols.add('PUBLISHED_ON')
            msg += "\n\tPUBLISHED_ON date should be greater than today for Scheduled Article"
    else:
        cleandata['PUBLISHED_ON'] = None
    # --------------------------------------------------------------------------
    if row['SEO_DESCRIPTION']:
        cleandata['SEO_DESCRIPTION'] = row['SEO_DESCRIPTION'][:160]
    else:
        cleandata['SEO_DESCRIPTION'] = row['DESCRIPTION'][:160]
    # --------------------------------------------------------------------------
    if row['SEO_TITLE']:
        cleandata['SEO_TITLE'] = row['SEO_TITLE'][:70]
    else:
        cleandata['SEO_TITLE'] = row['TITLE'][:70]
    # --------------------------------------------------------------------------
    if not row['SUMMARY']:
        valid = False
        invalidcols.add('SUMMARY')
        msg += "\n\tSUMMARY cannot be Empty"
    else:
        cleandata['SUMMARY'] = row['SUMMARY'][:250]
    # --------------------------------------------------------------------------
    if not row['TITLE']:
        valid = False
        invalidcols.add('TITLE')
        msg += "\n\tTITLE cannot be Empty"
    else:
        cleandata['TITLE'] = row['TITLE'][:200]
        if valid:
            cleandata['SLUG'] = getUniqueValue(Article, slugify(cleandata['TITLE']))
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
    
    return {"msg": msg, "valid": valid, "cleandata": cleandata, "invalidcols": invalidcols} 


@celery.task(name='tasks.process_articles_csv_upload')
def process_articles_csv_upload(csvfile):
    rownum, added, msg, invalidcols, user = 0, 0, "", set(), csvfile.uploaded_by
    rows = csv.DictReader(csvfile.file)
    csvfile.status = 'P'
    csvfile.save()
    for row in rows:
        if not set(row.keys()) == set(ARTICLE_CSV_HEADER):
            break
        rownum += 1
        cleandata = validate_and_clean(row, rownum)
        if not cleandata['valid']:
            msg += cleandata['msg'] + "\n"
            invalidcols.update(cleandata['invalidcols'])
        else:
            newobject = Article()
            newobject.article_type      = cleandata["cleandata"]['ARTICLE_TYPE']
            newobject.category          = cleandata["cleandata"]['CATEGORY']
            newobject.content           = cleandata["cleandata"]['DESCRIPTION']
            newobject.featured          = cleandata["cleandata"]['FEATURED']
            newobject.status            = cleandata["cleandata"]['STATUS']
            newobject.published_on      = cleandata["cleandata"]['PUBLISHED_ON']
            newobject.seo_description   = cleandata["cleandata"]['SEO_DESCRIPTION']
            newobject.seo_title         = cleandata["cleandata"]['SEO_TITLE']
            newobject.summary           = cleandata["cleandata"]['SUMMARY']
            newobject.title             = cleandata["cleandata"]["TITLE"]
            newobject.slug              = cleandata["cleandata"]["SLUG"]
            newobject.created_by        = newobject.modified_by = user
            newobject.save()
            for tag in cleandata["cleandata"]['TAGS']:
                newobject.tags.add(tag)
            added += 1
    if added == rownum:
        csvfile.status = 'S'
        csvfile.log = emailalert = "%d Articles has been added successfully.\n\n" % (rownum)
    else:
        csvfile.status = 'E'
        csvfile.log = emailalert = "%d Out of %d Articles has been added.\n\n" % (added, rownum)
    if invalidcols: csvfile.log += "The Columns " + str(tuple(invalidcols)) + " are having errors,\n\n"
    if not added: csvfile.status = 'E'
    csvfile.log += msg
    csvfile.save()
    try:
        emailalert = "<pre>"+emailalert+"</pre><br><a href='"+csvfile.get_log_url()+"'>Click here for more details</a>"
        email = EmailMessage('Article Adding via CSV', emailalert, my_settings.DEFAULT_FROM_EMAIL, [user.useremail])
        email.content_subtype = "html"
        email.send()
    except: pass
    if added:
        try: celery_rebuild_index.delay()
        except: pass
    return "Success"