# Create your views here.
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic.base import TemplateView
from django.template import Context
from faq.models import Faq
from datetime import datetime
from django.http import HttpResponseRedirect

def add_faq(request):
    x= Faq(created_on=datetime.now(),question='who are you?',answer='rajmohan')
    print x
    return render_to_response('success.html',context_instance=RequestContext(request))
