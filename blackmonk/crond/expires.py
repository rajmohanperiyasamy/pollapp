import datetime
from dateutil.relativedelta import relativedelta

import getsettings

from django.db.models import Count
from django.core import mail
from django.conf import settings as my_settings
from django.template import  Template,Context
from django.contrib.contenttypes.models import ContentType

from usermgmt.models import EmailTemplates
from common.getunique import getUniqueValue
from common.utils import get_global_settings

from sweepstakes.models import Sweepstakes, SweepstakesPoints, SweepstakesParticipant, SweepstakesParticipantPoints,SweepstakesSettings
from sweepstakes.utils import get_unique, get_contest_next_end_date
from business.models import Business, BusinessPrice
from classifieds.models import Classifieds, ClassifiedPrice
from events.models import Event, EventPrice, EventOccurence
from deal.models import Deal
from polls.models import Poll
from gallery.models import PhotoAlbum
from banners.models import BannerZones, BannerAdvertisements, BannerSections, BannerReports, BannerPayment
global_settings=get_global_settings()
today = datetime.date.today()
three_days_after = today + relativedelta(days= +3)
thirthy_days_before = today + relativedelta(days= -30)

SELECT_WINNER_ONLY_FOR_PUBLISHED_ITEMS = True

def process_business_expires():
	business = Business.objects.filter(status='P', lend_date=today).exclude(featured_sponsored='B')
	business.update(featured_sponsored='B')
	business.update(payment=BusinessPrice.objects.get(level='level0'))
	
def process_classifieds_expires():
	classifieds = Classifieds.objects.filter(status='P', listing_end_date__lt=today).update(status='E')

def process_deal_expires():	
	deals = Deal.objects.filter(status='P', end_date__lte=today).update(status='E')
	
def process_event_expires():
	events = Event.objects.filter(status='P', end_date__lt=today).update(status='E')
	
	events = Event.objects.filter(status='P', listing_end__lt=today).exclude(listing_type='B')
	events.update(listing_type='B')
	events.update(payment=EventPrice.objects.get(level='level0'))

def process_polls_expires():
	polls = Poll.objects.filter(status='P', expiry_date__lt=today)
	if polls:
		polls.update(status='E')
		try:
			current_poll = Poll.objects.filter(status='N', expiry_date__gte=today)[0]
			current_poll.status = 'P'
			current_poll.save()
		except:pass


def process_banners():
	''' for expired banners '''
	try:
	    banners = BannerAdvertisements.objects.annotate(imp_count = Count('banner_report')).filter(status='P')
	    
	    for b in banners:
        	if b.imp_count > b.impressions:
				b.status = 'E'
				b.total_amount = 0
				b.impressions = 0
	        b.save()
	except:pass
	"""
    #for unpaid imressions
	try:
		banners = BannerAdvertisements.objects.filter(status='P')
		paid_banner = PaymentOrder.objects.filter(content_type=ct,object_id = banner_obj.id)
		tot = 0
		for bans in paid_banner:
		    tot = tot+bans.amount
	except:pass
    """    
def get_next_day(event,today):
   occ_objs = EventOccurence.objects.filter(event=event).order_by('id')
   for occ_obj in occ_objs:
       if occ_obj.date >= today:
           return occ_obj.date
   return False

def update_event_startdate():
    try:
        events = Event.objects.filter(status='P', is_reoccuring = True,start_date__lte = today)
        for event in events:
           if get_next_day(event,today): 
               event.start_date = get_next_day(event,today)
               event.save()
    except:pass
    
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
	
def winner_choice(possible_winners, total_winners):
	winners = []
	flag = True
	while flag:
		w = choice(possible_winners)
		if w not in winners:winners.append(w)
		if len(winners) == total_winners:flag = False
		if choice(possible_winners) < total_winners:
			winners = list(set(possible_winners))
			flag = False
	return SweepstakesParticipantPoints.objects.filter(id__in=winners)
		
def send_mail_to_winners(winners,email):
	mail_list=[]
	for	w in winners:
		to_emailids=[w.participant.email]
		email_temp=EmailTemplates.objects.get(code='cwm')
		s=Template(email_temp.subject)
		t=Template(email_temp.template)
		
		data={
			'USERNAME':w.participant.first_name(),
			'CONTEST_TITLE':w.sweepstakes.title,
			'CONTEST_ID':w.sweepstakes.contest_id,
			'CONTEST_URL':global_settings.website_url+reverse('sweepstakes_detail',args=[w.sweepstakes.id,w.sweepstakes.slug]),
			'CONTEST_HOME_URL':global_settings.website_url+reverse('sweepstakes_home'),
			'WEBSITE':global_settings.domain
		}
		c=Context(data)
		email_message = t.render(c)
		subject = s.render(c)
		
		email = mail.EmailMessage(subject, email_message, from_email, to_emailids,headers = {'Reply-To': 'another@example.com'})
		email.content_subtype = "html"
		
		mail_list.append(email)
	connection.send_messages(mail_list)
	return True
	
def select_winners(contests):
	#######################################################
	connection = mail.get_connection()
	connection.open()
	try:email=SweepstakesSettings.objects.all()[0].email
	except:email=my_settings.DEFAULT_FROM_EMAIL
	#######################################################
	for contest in contests:
		allusers = SweepstakesParticipant.objects.filter(sweepstakes=contest)
		possible_winners = []
		for user in allusers:
			points = SweepstakesParticipantPoints.objects.filter(sweepstakes=user)
			if not SELECT_WINNER_ONLY_FOR_PUBLISHED_ITEMS:
				for p in points:
					for usr_pt in range(user.total):possible_winners.append(user.id)
			else:
				for usr_pt in range(user.reg_point):possible_winners.append(user.id)
				for usr_pt in range(user.fb_point):possible_winners.append(user.id)
				for usr_pt in range(user.friend_point):possible_winners.append(user.id)
				for usr_pt in range(user.comments):possible_winners.append(user.id)
				for p in points:
					try:
						model=ContentType.objects.get_for_id(p.content_type)
						obj=model.get_object_for_this_type(id=p.object_id)
						try:
							if obj.status=='P':
								for usr_pt in range(p.user_point):possible_winners.append(user.id)
						except AttributeError:
							for usr_pt in range(p.user_point):possible_winners.append(user.id)
						except:pass
					except:pass
			
		winner = winner_choice(possible_winners, contest.total_winners)
		for w in winner:contest.winner.add(w)
		send_mail_to_winners(emails,email)
	#######################################################
	connection.close()
	return True
	#######################################################
		
def duplicate_contest(contests):
	for contest in contests:
		if contest.duration!='N':
			cont = Sweepstakes()
			cont.title = contest.title
			cont.slug = getUniqueValue(Sweepstakes, slugify(contest.slug))
			cont.description = contest.description
			cont.image = contest.image
			cont.duration = contest.duration
			cont.static_page = contest.static_page
			cont.sweepstakes_id = contest.sweepstakes_id
			cont.start_date = today#contest.start_date
			cont.end_date = contest.end_date
			cont.total_winners = contest.total_winners
			cont.select_winners_on = contest.select_winners_on
			cont.seo_title = contest.seo_title
			cont.seo_description = contest.seo_description
			cont.contest_id = get_unique('CI')
			cont.reg_point = contest.reg_point
			cont.fb_point = contest.fb_point
			cont.friend_point = contest.friend_point
			cont.comments = contest.comments
			cont.advice_e = contest.advice_e
			cont.discussions_e = contest.discussions_e
			cont.created_by = cont.modified_by = contest.created_by
			cont.created_on = cont.modified_on = today
			cont.status = 'P'
			cont.save()
			cont.current_end_date = get_contest_next_end_date(cont)
			points = SweepstakesPoints.objects.filter(sweepstake=contest)
			for point in points:
				p = SweepstakesPoints(sweepstake=cont, app=point.app)
				p.app_point = point.app_point
				p.save
				cont.settings.add(p)
			cont.save()
	return True
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
def process_sweepstakes_expires_select_winners():
	contest = Sweepstakes.objects.filter(status='P', end_date__lt=today)
	contest.update(status='E')
	select_winners(contest)
	rcontest = Sweepstakes.objects.filter(status='P', current_end_date__lt=today)
	rcontest.update(status='E')
	select_winners(rcontest)
	duplicate_contest(rcontest)

"""
process_business_expires()
process_classifieds_expires()
process_deal_expires()
process_event_expires()
process_polls_expires()
process_sweepstakes_expires_select_winners()
"""
process_banners()
update_event_startdate()