from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render_to_response

from common.models import AvailableApps

class CheckApps(object):
	def process_response(self, request, response):
		try:
			slug = request.META['PATH_INFO'] .split('/')[1]
			try:slug1 = request.META['PATH_INFO'] .split('/')[2]
			except:slug1 = False
		except:slug1 = slug = None
		
		inactive_apps=AvailableApps.get_inactive_app_slug()
		
		if slug in settings.RESTRICTED_URL or slug1 in settings.RESTRICTED_URL or slug in inactive_apps or slug1 in inactive_apps:
			return render_to_response('404.html')
		else:return response
