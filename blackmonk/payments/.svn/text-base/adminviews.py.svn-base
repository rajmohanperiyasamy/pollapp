from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson

from common.forms import GeneralPayment
from common.models import PaymentConfigure, CommonConfigure
from common.static_msg import CONFIG_MSG
from common.templatetags.ds_utils import get_msg_class_name
from usermgmt.decorators import admin_required


@admin_required
def configuration_payment(request):
    payment = PaymentConfigure.objects.all()[:1]
    if payment:
        payment = payment[0]
    else:
        payment = None
    if request.method == "POST":
        form = GeneralPayment(request.POST, instance=payment)
        if form.is_valid():
            general = form.save()
            try:
                common = CommonConfigure.objects.all()[:1][0]
                common.currency = general.currency_symbol
                common.save()
            except:
                pass
        html = render_to_string('admin/configuration/include_payment.html', {'form': form, 'payment': payment})
        data = {'html': html, 'msg': str(CONFIG_MSG['PSUS']), 'mtype': get_msg_class_name('s')}
        return HttpResponse(simplejson.dumps(data))
    else:
        payment = PaymentConfigure.objects.all()[:1]
        if payment:
            payment = payment[0]
        else:
            payment = None
        form = GeneralPayment(instance=payment)
        data = {'form': form, 'payment': payment}
        return render_to_response ('admin/configuration/payment.html', data, context_instance=RequestContext(request))
        
