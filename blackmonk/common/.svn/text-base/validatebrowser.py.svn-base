from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

ALLOWED_BROWSERS = (
	('Firefox', 3.5),
	('Opera', 9),
	('MSIE', 7),
	('Safari', 85),
	('Chrome', 20),
)

def check_browser(agent):
	for b in ALLOWED_BROWSERS:
		loc = agent.find(b[0])
		if loc != -1:
			start = loc+len(b[0])+1
			end = agent.find(' ', start)
			
			if end != -1:version = agent[start:end]
			else:version = agent[start:]
			
			if version == '':version = '2.0'
			elif version[-1] == ';':version = version[0:-1]
			
			version = version.split('.')
			version = "%s.%s" % (version[0].split(')')[0], ''.join(version[1:]).split(',')[0].split('+')[0].split('u')[0].split('a')[0])
			
			if float(version) < float(b[1]):valid = False
			else:valid = True
			
			return {'browser_version': version, 'browser': b[0], 'valid': valid}
	return {'browser': agent, 'browser_version': '', 'valid': True}

class ValidateBrowser(object):
	def process_response(self, request, response):
		if '_verify_browser' in request.COOKIES or request.META['HTTP_USER_AGENT'] == 'Python-urllib/1.16' or request.GET.get('skipcheck', False) or request.META['HTTP_USER_AGENT'].find('Googlebot') != -1:
			return response
		
		agent = request.META['HTTP_USER_AGENT']
		ec = check_browser(agent)	
		
		if ec['valid']==True:
			response.set_cookie('_verify_browser', '1', max_age=60*60*24*30, domain=settings.SESSION_COOKIE_DOMAIN)
			return response
		else:
			return render_to_response('browser_not_supported.html',context_instance=RequestContext(request))
