from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
import stripe

from common.getunique import getUniqueValue
from common.models import PaymentConfigure
from payments.stripes.models import StripePaymentDetails, StripePlanDetails


def stripe_add_plan(request):
    data = {}
    currency = PaymentConfigure.get_payment_settings()
    stripe.api_key = currency.stripe_private_key
    if request.POST:
        try:
            Type = request.POST.get("type")
            try:
                oldplan = StripePlanDetails.objects.get(type = Type)
                if oldplan:
                    oldplan.type = 'uncategorized'
                    oldplan.status = "I"
                    oldplan.save()
            except:
                pass
                
            plan = StripePlanDetails()
            name = request.POST.get("name")
            slug = getUniqueValue(model=StripePlanDetails,proposal = slugify(name), field_name ="plan_id" )
            
            plan.name =request.POST.get("name")
            plan.currency = request.POST.get("currency")
            plan.amount = float(request.POST.get("amount"))
            plan.interval = request.POST.get("interval")
            plan.type = request.POST.get("type")
            plan.status = "A"
            plan.plan_id = slug
            plan.save()
            
            stripeplan = stripe.Plan.create(amount=(int(plan.amount*100)), interval=plan.interval, name=plan.name, currency=plan.currency, id=plan.plan_id)           
            
            return HttpResponseRedirect(reverse('stripe_list_plans')+'?msg=Plan Added Successfully')
        except:
            return HttpResponseRedirect(reverse('stripe_list_plans')+'?msg=Error in adding Plan')
    else:
        return render_to_response("payments/stripe/stripe_add_subscription_plan.html", data, context_instance=RequestContext(request))

def stripe_list_plans(request):
    data ={}
    currency=PaymentConfigure.get_payment_settings()
    stripe.api_key = currency.stripe_private_key
    data['plans'] = StripePlanDetails.objects.all()
    return render_to_response("payments/stripe/stripe-list-plans.html", data, context_instance=RequestContext(request))

def stripe_plan_details(request, id):
    data={}
    plan = StripePlanDetails.objects.get(id = id)
    data['plan'] = plan
    return render_to_response("payments/stripe/stripe_plan_details.html", data, context_instance=RequestContext(request))
