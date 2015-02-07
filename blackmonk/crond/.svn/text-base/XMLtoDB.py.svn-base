#! /home/blackmonk/virtualenvs/bm/bin/python
import getsettings
from django.utils import simplejson
from django.contrib.auth import get_user_model
User = get_user_model()
import datetime,time
from datetime import timedelta

from usermgmt.models import *
from article.models import *
from business.models import *
from business.models import Tag as BusinessTag
from common.models import Address
article_json = open('article.json')
profile_json = open('profile.json')
business_json = open('business.json')

art = False
prof = False
bus = True
#User Management
if profile_json != [] and prof:
    datas = simplejson.load(profile_json)
    for data in datas:
        if data['model'] == 'usermgmt.profile':
            profile = Profile(pk=data['pk'])
            user = User.objects.get(pk=data['pk'])
            profile.user = user
            if data['fields']['firstname'] and data['fields']['lastname']:
                display_name = data['fields']['firstname']+' '+data['fields']['lastname'] 
            elif data['fields']['firstname']:
                display_name = data['fields']['firstname'] 
            else:display_name = user.username     
            profile.display_name=display_name
            profile.birthdate=data['fields']['birthdate']
            profile.about=data['fields']['about']
            profile.location=data['fields']['location']
            profile.not_in_city=data['fields']['not_in_city']
            profile.address=data['fields']['address']
            profile.zip=data['fields']['pin']
            profile.lat=data['fields']['lat']
            profile.lon=data['fields']['lon']
            profile.zoom=data['fields']['map_zoom']
            profile.mobile=data['fields']['mobile']
            profile.phone=data['fields']['phone']
            profile.occupation=data['fields']['occupation']
            profile.gender=data['fields']['gender']
            profile.married=data['fields']['married']
            profile.impact=data['fields']['impact']
            profile.signature=data['fields']['signature']
            profile.forum_post_count=data['fields']['forum_post_count']
            profile.save()
    for data in datas:    
        if data['model'] == 'usermgmt.profileprivacy':
            privacy = ProfilePrivacy(pk=data['pk'])
            privacy.profile=Profile.objects.get(pk=data['pk'])
            privacy.show_sex=data['fields']['show_sex']
            privacy.show_birthdate=data['fields']['show_birthdate']
            privacy.show_email=data['fields']['show_email']
            privacy.show_links=data['fields']['show_links']
            privacy.show_screen=data['fields']['show_screen']
            privacy.show_contact=data['fields']['show_contact']
            privacy.show_occupation=data['fields']['show_occupation']
            privacy.show_married=data['fields']['show_married']
            privacy.save()
    for data in datas:    
        if data['model'] == 'usermgmt.emailsetting':
            email_settings = EmailSetting(pk=data['pk'])
            email_settings.user=User.objects.get(pk=data['pk'])
            email_settings.qa_reply=data['fields']['qa_reply']
            email_settings.profile_update=data['fields']['profile_update']
            email_settings.classified_reply=data['fields']['classified_reply']
            email_settings.article_comment=data['fields']['article_comment']
            email_settings.business_comment=data['fields']['business_comment']
            email_settings.save()
    for data in datas:    
        if data['model'] == 'usermgmt.avatar':
            profile=Profile.objects.get(pk=data['fields']['user'])
            profile.image=data['fields']['image']
            profile.save()
    
# Article    
if article_json != [] and art:
    datas = simplejson.load(article_json)
    for data in datas:
        if data['model'] == 'article.tag':
            tag = Tag(pk=data['pk'])
            tag.tag = data['fields']['tag']
            tag.save()
    for data in datas:
        if data['model'] == 'article.articlecategory':   
            category = ArticleCategory(pk=data['pk'])
            category.name=data['fields']['name']
            category.slug=data['fields']['slug']
            category.seo_title=data['fields']['seo_title']
            category.save()
    for data in datas:    
        if data['model'] == 'article.article':   
            article = Article(pk=data['pk'])
            article.title=data['fields']['title']
            article.slug=data['fields']['slug']
            article.seo_title=data['fields']['seo_title']
            article.seo_description=data['fields']['seo_description']    
            article.summary=data['fields']['summary']    
            article.content=data['fields']['content']    
            article.featured=data['fields']['featured']    
            article.most_viewed=data['fields']['most_viewed']    
            article.published_on=data['fields']['published_on']     
            
            article.created_on=data['fields']['created_on']  
            article.modified_on=data['fields']['modified_on']   
            article.is_active = data['fields']['is_active']   
            article.status = data['fields']['status']   
            
            try:
                user=User.objects.get(pk=data['fields']['created_by']  )
                article.created_by=user
            except:
                user=User.objects.get(pk=1)
                article.created_by=user
            try:
                user=User.objects.get(pk=data['fields']['modified_by']  )
                article.modified_by=user
            except:
                user=User.objects.get(pk=1)
                article.modified_by=user    
            try:
                cat_obj = ArticleCategory.objects.get(pk=data['fields']['category'])
                article.category=cat_obj
            except:
                cat_obj = ArticleCategory.objects.get(pk=1)
                article.category=cat_obj
            article.save()        
            for tag in data['fields']['tags']:
                 try:
                     objtag = Tag.objects.get(pk=tag)
                     article.tags.add(objtag)
                 except:pass
    
if business_json != [] and bus:
    datas = simplejson.load(business_json)
    for data in datas:
        if data['model'] == 'business.tag':
            tag = BusinessTag(pk=data['pk'])
            tag.tag = data['fields']['tag']
            tag.save()
    for data in datas:
        if data['model'] == 'business.businesscategory':
            if not data['fields']['parent_cat']:
                cat = BusinessCategory(pk=data['pk'])
                cat.name = data['fields']['name']
                cat.parent_cat = data['fields']['parent_cat']
                cat.slug = data['fields']['slug']
                cat.seo_title = data['fields']['seo_title']
                cat.seo_description = data['fields']['seo_description']
                cat.price_year = data['fields']['price_year']
                cat.price_month = data['fields']['price_month']
                cat.save()
    for data in datas:
        if data['model'] == 'business.businesscategory':    
            if data['fields']['parent_cat']:
                cat = BusinessCategory(pk=data['pk'])
                parent_cat = BusinessCategory.objects.get(pk=data['fields']['parent_cat'])
                cat.parent_cat = parent_cat
                cat.name = data['fields']['name']
                cat.slug = data['fields']['slug']
                cat.seo_title = data['fields']['seo_title']
                cat.seo_description = data['fields']['seo_description']
                cat.price_year = data['fields']['price_year']
                cat.price_month = data['fields']['price_month']
                cat.save()
                
    for data in datas:
        if data['model'] == 'business.attributes':
            attribute_grp = AttributeGroup(pk=data['pk'])
            attribute_grp.name = data['fields']['name']
            attribute_grp.display_position = data['fields']['posion']
            attribute_grp.save()   
              
    for data in datas:
        if data['model'] == 'business.attributekey':
            attribute = Attributes(pk=data['pk'])
            attribute.name = data['fields']['name']
            attribute.type = data['fields']['type']
            attribute.staff_created = data['fields']['staff_created']
            attribute.attribute_group = AttributeGroup.objects.get(pk=data['fields']['attribute'])
            for atr in datas:
                if atr['model'] == 'business.attributes':
                    if atr['pk']==data['fields']['attribute']:
                        attribute.category = BusinessCategory.objects.get(pk=atr['fields']['category'])
            attribute.save()              
              
    for data in datas:
        if data['model'] == 'business.attributevalue':
            attribute_val = AttributeValues(pk=data['pk'])
            attribute_val.staff_created = data['fields']['staff_created']
            attribute_val.name = data['fields']['name']
            attribute_val.attribute_key = Attributes.objects.get(pk=data['fields']['attribute_key'])
            attribute_val.save()     
    
    for data in datas:
        if data['model'] == 'business.paymentoptions':
            payment_option = PaymentOptions(pk=data['pk'])
            payment_option.name = data['fields']['name']
            payment_option.image_position = data['fields']['image_position']
            payment_option.save()
    
    for data in datas:
        if data['model'] == 'business.business':
            business = Business(pk=data['pk'])
            business.name = data['fields']['name']
            business.slug = data['fields']['slug']
            business.operating_hours = data['fields']['operating_hours']
            business.summary = data['fields']['summary']
            business.description = data['fields']['description']
            business.specialofferimage = data['fields']['specialofferimage']
            business.specialofferurl = data['fields']['specialofferurl']
            business.introductions = data['fields']['introductions']
            business.votes = data['fields']['votes']
            business.ratings = data['fields']['ratings']
            business.most_viewed = data['fields']['most_viewed']
            business.seo_title = data['fields']['seo_title']
            
            business.seo_description = data['fields']['seo_description']
            business.featured_sponsored = data['fields']['featured_sponsored']
            business.lstart_date = datetime.datetime.now()
            business.lend_date = datetime.datetime.now()+timedelta(days=180)
            business.created_on = data['fields']['created_on']
            business.modified_on = data['fields']['modified_on']
            business.is_active = data['fields']['is_active']
            business.status = data['fields']['status']
           
            business.payment_type = data['fields']['payment_type']
            business.is_paid = data['fields']['is_paid']
            
            if data['fields']['payment']:
                business.payment = BusinessPrice.objects.get(pk=data['fields']['payment'])
            
            business.created_by = User.objects.get(pk=data['fields']['created_by'])
            business.modified_by = User.objects.get(pk=data['fields']['modified_by'])
            business.save()       
            
            for tag in data['fields']['tags']:
                 try:
                     objtag = BusinessTag.objects.get(pk=tag)
                     business.tags.add(objtag)
                 except:pass
            try:
                objtag = BusinessCategory.objects.get(pk=data['fields']['category'])
                business.tags.add(objtag)
            except:pass     
              
            if data['fields']['logo_active']:
                bus_logo = BusinessLogo(pk=data['pk'])
                bus_logo.logo = data['fields']['logo']
                bus_logo.save()  
            for pay_opt in data['fields']['paymentoptions']:
                 try:
                     payment_optionobj = PaymentOptions.objects.get(pk=pay_opt)
                     business.paymentoptions.add(payment_optionobj)
                 except:pass  
              
    for data in datas:
        if data['model'] == 'business.workinghours':
            workig_hours = WorkingHours(pk=data['fields']['business'])
            workig_hours.notes = data['fields']['notes']
            workig_hours.mon_start = data['fields']['mon_start']
            workig_hours.mon_end = data['fields']['mon_end']
            workig_hours.tue_start = data['fields']['tue_start']
            workig_hours.tue_end = data['fields']['tue_end']
            workig_hours.wed_start = data['fields']['wed_start']
            workig_hours.wed_end = data['fields']['wed_end']
            workig_hours.thu_start = data['fields']['thu_start']
            workig_hours.thu_end = data['fields']['thu_end']
            workig_hours.fri_start = data['fields']['fri_start']
            workig_hours.fri_end = data['fields']['fri_end']
            workig_hours.sat_start = data['fields']['sat_start']
            workig_hours.sat_end = data['fields']['sat_end']
            workig_hours.sun_start = data['fields']['sun_start']
            workig_hours.sun_end = data['fields']['sun_end']
            workig_hours.status = data['fields']['status']
            workig_hours.save()    
            business = Business.objects.get(pk=data['fields']['business'])   
            business.workinghours = workig_hours
            business.save()
    for data in datas:
        if data['model'] == 'business.sponsoredprice':
            sponsored_price = SponsoredPrice(pk=data['pk'])
            sponsored_price.category = BusinessCategory.objects.get(pk=data['fields']['category'])
            sponsored_price.pay_month = data['fields']['pay_month']
            sponsored_price.price = data['fields']['price']
            sponsored_price.currency = data['fields']['currency']
            sponsored_price.save()   
              
    for data in datas:
        if data['model'] == 'business.businessreview':
            if not data['fields']['parent']:
                bus_review = BusinessReview(pk=data['pk'])
                bus_review.subject = data['fields']['subject']
                bus_review.name = data['fields']['name']
                bus_review.email = data['fields']['email']
                bus_review.ratings = data['fields']['ratings']
                bus_review.abuse_count = data['fields']['abuse_count']
                bus_review.like_count = data['fields']['like_count']
                bus_review.status = data['fields']['status']
                bus_review.approved_on = data['fields']['approved_on']
                try:bus_review.created_by = User.objects.get(pk=data['fields']['created_by'])
                except:pass
                bus_review.created_on = data['fields']['created_on']
                bus_review.business = Business.objects.get(pk=data['fields']['business'])   
                bus_review.save()   
                       
    for data in datas:
        if data['model'] == 'business.businessreview':
            if data['fields']['parent']:
                bus_review = BusinessReview(pk=data['pk'])
                bus_review.parent = BusinessReview.objects.get(pk=data['fields']['parent'])
                bus_review.subject = data['fields']['subject']
                bus_review.name = data['fields']['name']
                bus_review.email = data['fields']['email']
                bus_review.ratings = data['fields']['ratings']
                bus_review.abuse_count = data['fields']['abuse_count']
                bus_review.like_count = data['fields']['like_count']
                bus_review.status = data['fields']['status']
                bus_review.approved_on = data['fields']['approved_on']
                try:bus_review.created_by = User.objects.get(pk=data['fields']['created_by'])
                except:pass
                bus_review.created_on = data['fields']['created_on']
                bus_review.business = Business.objects.get(pk=data['fields']['business'])   
                bus_review.save()   
                  
    for data in datas:
        if data['model'] == 'business.address':
            bus_address = Address(pk=data['pk'])
            bus_address.business = Business.objects.get(pk=data['fields']['business'])
            bus_address.status = data['fields']['status']
            bus_address.address1 = data['fields']['address1']
            bus_address.address2 = data['fields']['address2']
            bus_address.zip = data['fields']['pin']
            bus_address.city = data['fields']['city']
            bus_address.telephone1 = data['fields']['telephone']
            bus_address.fax = data['fields']['fax']
            bus_address.mobile = data['fields']['mobile']
            bus_address.email = data['fields']['email']
            bus_address.website = data['fields']['website']
            bus_address.lat = data['fields']['lat']
            bus_address.lon = data['fields']['lon']
            bus_address.zoom = data['fields']['map_zoom']
            bus_address.save()            
              
    for data in datas:
        if data['model'] == 'business.bizattributes':
            biz_attributes = BizAttributes(pk=data['pk'])
            biz_attributes.business = Business.objects.get(pk=data['fields']['business'])
            biz_attributes.key = Attributes.objects.get(pk=data['fields']['key'])
            biz_attributes.save() 
            for val in data['fields']['value']:
                 try:
                     attr_val_obj = AttributeValues.objects.get(pk=val)
                     biz_attributes.value.add(attr_val_obj)
                 except:pass              
              
              