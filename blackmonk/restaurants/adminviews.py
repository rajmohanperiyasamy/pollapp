#Django
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.forms.models import modelformset_factory
from django.db.models import Count
from django.contrib import messages
from usermgmt.decorators import admin_required
from common.templatetags.ds_utils import get_msg_class_name

from common.static_msg import RESTAURANT_MSG, MEALTYPES_MSG, CUISINES_MSG, FEATURE_MSG, REST_PAYMENT_MSG
from common.admin_utils import success_response_to_save_category,error_response,response_delete_category
from common.admin_utils import success_response_to_save_category,response_delete_category,error_response,response_to_save_settings
from common.forms import ApprovalSettingForm,SEOForm
from common.models import ModuleNames, ApprovalSettings
from common.admin_utils import save_emailsettings, get_emailsettings
from common.getunique import getUniqueValue

from restaurants.models import RestaurantCategories, Restaurants, MealTypes, Cuisines, RestaurantFeatures, PaymentOptions, RestaurantPrice
from restaurants.adminforms import RestaurantCategoriesForm, MealTypesForm, CuisinesForm,  RestaurantFeaturesForm, PaymentOptionsForm, RestaurantPriceForm

from restaurants.restaurant_utils import success_response_to_restaurant_module

ARTICLE_MSG="passing hardcode string"
#==========================================================================================
@admin_required
def restaurants_settings(request, template='admin/portal/restaurants/setting.html'):
    active=inactive=0
    approval=None
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
    
    category=RestaurantCategories.objects.all().count()
    print category
    
    restaurant_state = Restaurants.objects.values('is_active','status').annotate(s_count=Count('status'),a_count=Count('is_active'))
    
    for st in restaurant_state:
        print st , STATE[st['status']]
        STATE[st['status']]+=st['s_count']
        if st['is_active']:
            active+=st['a_count']
        else:
            inactive+=st['a_count']
      
    data={
          'restaurants':inactive+active,
          'active':active,
          'category':category,
    }
    
    try:
        approval = ApprovalSettings.objects.get(name='restaurants')
        approval_form=ApprovalSettingForm(instance=approval)
    except:approval_form=ApprovalSettingForm()
    try:seo = ModuleNames.get_module_seo(name='restaurants')
    except:seo = ModuleNames(name='restaurants')
    if request.method=='POST':
        if approval:approval_form=ApprovalSettingForm(request.POST,instance=approval)
        else:approval_form=ApprovalSettingForm(request.POST)
        seo_form = SEOForm(request.POST)
        if approval_form.is_valid() and seo_form.is_valid():
            approvals=approval_form.save(commit=False)
            if not approval:approvals.name='restaurants'
            approvals.modified_by=request.user
            approvals.save()

            seo.seo_title = seo_form.cleaned_data.get('meta_title')
            seo.seo_description = seo_form.cleaned_data.get('meta_description')
            seo.modified_by = request.user
            seo.save()
            save_emailsettings(request,'restaurants')
            extra_data = {'seo':seo,'seo_form':seo_form,'approval_form':approval_form,'emailsettings':get_emailsettings('restaurants')}
            data.update(extra_data)
            return response_to_save_settings(request,True,data,'admin/portal/restaurants/include_settings.html',RESTAURANT_MSG)
        else:
            extra_data = {'seo':seo,'seo_form':seo_form,'approval_form':approval_form,'emailsettings':get_emailsettings('restaurants')}
            data.update(extra_data)
            return response_to_save_settings(request,False,data,'admin/portal/restaurants/include_settings.html',RESTAURANT_MSG)

    extra_data = {'seo':seo,'approval_form':approval_form,'emailsettings':get_emailsettings('restaurants')}
    data.update(extra_data)
    
    return render_to_response (template, data, context_instance=RequestContext(request))





#============================================ category section

@admin_required
def restaurants_category(request, template='admin/portal/restaurants/category.html'):
    cat = RestaurantCategories.objects.order_by('name')
    data={'categoryes':cat}
    return render_to_response (template, data, context_instance=RequestContext(request))


@admin_required
def restaurants_category_update(request,template='admin/portal/restaurants/update_category.html'):
    print "in........restaurants_category_update"
    data={}
    category=None
    try:
        category = RestaurantCategories.objects.get(id = request.REQUEST['id'])
        form=RestaurantCategoriesForm(instance=category)
    except:
        form=RestaurantCategoriesForm()
        print "1111.."
    if request.method == "POST":
        if category:
            form=RestaurantCategoriesForm(request.POST,instance=category)
            print "222.."
        else: 
            form=RestaurantCategoriesForm(request.POST)
            print "333.."
        
        if form.is_valid():
            cat_form=form.save()
            form=RestaurantCategoriesForm()  
            data = {'form':form,'cat':category}
            append_data={'cat':cat_form,'edit_url':reverse('admin_portal_restaurants_category_update')}
            print "return success"
            return success_response_to_save_category(append_data,data,template, RESTAURANT_MSG)
        else:
            data = {'form':form,'cat':category}
            return error_response(data, template, RESTAURANT_MSG)
    else:
        data = {'form':form,'cat':category}
        return render_to_response(template, data, context_instance=RequestContext(request))

@admin_required
def restaurants_category_delete(request):
    data=response_delete_category(request,RestaurantCategories, RESTAURANT_MSG)
    #.... data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return HttpResponse(simplejson.dumps(data)) 












#===================================== meal section    
@admin_required
def restaurants_mealtypes(request, template='admin/portal/restaurants/mealtypes.html'):
    cat = MealTypes.objects.order_by('name')
    data={'categoryes':cat}
    return render_to_response (template, data, context_instance=RequestContext(request))



@admin_required
def restaurants_mealtypes_update(request,template='admin/portal/restaurants/update_mealtypes.html'):
    print "in........restaurants_mealtypes_update"
    data={}
    category=None
    try: 
        
        category = MealTypes.objects.get(id = request.REQUEST['id'])
        form=MealTypesForm(instance=category)
    except:
        form=MealTypesForm()
        print "1..."
    if request.method == "POST":
        if category:
            print "2.."
            form=MealTypesForm(request.POST,instance=category)
        else: 
            print "3.."
            form=MealTypesForm(request.POST)
        
        if form.is_valid():
            cat_form=form.save(commit=False)
            cat_form.created_by = cat_form.modified_by = request.user
            cat_form.status = 'P'
            cat_form.save()
            form=MealTypesForm() #.. that will show the empty form when 'save & another chosen
            data = {'form':form,'cat':category}
            append_data={'cat':cat_form,'edit_url':reverse('admin_portal_restaurants_mealtypes_update'), 'label': 'Update Meal Type'}
            print "return..."
            return success_response_to_restaurant_module(append_data,data,template, MEALTYPES_MSG)
        else:
            data = {'form':form,'cat':category}
            return error_response(data, template, MEALTYPES_MSG)
    else:
        data = {'form':form,'cat':category}
        return render_to_response(template, data, context_instance=RequestContext(request))


@admin_required
def restaurants_mealtypes_delete(request):
    data=response_delete_category(request,MealTypes, MEALTYPES_MSG)
    #.... data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return HttpResponse(simplejson.dumps(data)) 


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 #=============================================   Cuisines
@admin_required
def restaurants_cuisines(request, template='admin/portal/restaurants/cuisines.html'):
    cat = Cuisines.objects.order_by('name')
    data={'categoryes':cat}
    return render_to_response (template, data, context_instance=RequestContext(request))



@admin_required
def restaurants_cuisines_update(request,template='admin/portal/restaurants/update_cuisines.html'):
    print "in........restaurants_cuisines_update"
    data={}
    category=None
    try: 
        print "try"
        category = Cuisines.objects.get(id = request.REQUEST['id'])
        form=CuisinesForm(instance=category)
    except:
        print "form.errors"
        form=CuisinesForm()
    if request.method == "POST":
        if category:
            print "if_1"
            form=CuisinesForm(request.POST,instance=category)
        else: 
            print "else_1"
            form=CuisinesForm(request.POST)
        
        if form.is_valid():
            cat_form=form.save(commit=False)
            cat_form.created_by = cat_form.modified_by = request.user
            cat_form.slug = getUniqueValue(Cuisines,slugify(cat_form.name),instance_pk=cat_form.id)
            cat_form.status = 'P'
            cat_form.save()
            form=CuisinesForm()  #.. that will show the empty form when 'save & another chosen
            data = {'form':form,'cat':category}
            append_data={'cat':cat_form,'edit_url':reverse('admin_portal_restaurants_cuisines_update'), 'label': 'Update Cuisine'}
            return success_response_to_restaurant_module(append_data, data, template, CUISINES_MSG)
        else:
            data = {'form':form,'cat':category}
            return error_response(data, template, CUISINES_MSG)
    else:
        print "Get"
        data = {'form':form,'cat':category}
        return render_to_response(template, data, context_instance=RequestContext(request))


@admin_required
def restaurants_cuisines_delete(request):
    data=response_delete_category(request,Cuisines, CUISINES_MSG)
    #.... data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return HttpResponse(simplejson.dumps(data)) 







#============================================ feature section

@admin_required
def restaurants_feature(request, template='admin/portal/restaurants/feature.html'):
    print "feature......."
    cat = RestaurantFeatures.objects.order_by('name')
    data={'categoryes':cat}
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def restaurants_feature_update(request,template='admin/portal/restaurants/update_feature.html'):
    print "in........restaurants_feature_update"
    data={}
    category=None
    try: 
        print "try"
        category = RestaurantFeatures.objects.get(id = request.REQUEST['id'])
        form=RestaurantFeaturesForm(instance=category)
    except:
        print "form.errors"
        form=RestaurantFeaturesForm()
    if request.method == "POST":
        if category:
            print "if_1"
            form=RestaurantFeaturesForm(request.POST,instance=category)
        else: 
            print "else_1"
            form=RestaurantFeaturesForm(request.POST)
        
        if form.is_valid():
            cat_form=form.save(commit=False)
            cat_form.created_by = cat_form.modified_by = request.user
            cat_form.status = 'P'
            cat_form.save()
            form=RestaurantFeaturesForm()  #.. that will show the empty form when 'save & another chosen
            data = {'form':form,'cat':category}
            append_data={'cat':cat_form,'edit_url':reverse('admin_portal_restaurants_feature_update'), 'label': 'Update Feature'}
            return success_response_to_restaurant_module(append_data, data, template, FEATURE_MSG)
        else:
            data = {'form':form,'cat':category}
            return error_response(data, template, FEATURE_MSG)
    else:
        print "Get"
        data = {'form':form,'cat':category}
        return render_to_response(template, data, context_instance=RequestContext(request))
    
    
@admin_required
def restaurants_feature_delete(request):
    data=response_delete_category(request,RestaurantFeatures, FEATURE_MSG)
    #.... data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return HttpResponse(simplejson.dumps(data))



#============================================ payment section

@admin_required
def restaurants_payment(request, template='admin/portal/restaurants/payment.html'):
    print "feature......."
    cat = PaymentOptions.objects.order_by('name')
    data={'categoryes':cat}
    return render_to_response (template, data, context_instance=RequestContext(request))



@admin_required
def restaurants_payment_update(request,template='admin/portal/restaurants/update_payment.html'):
    print "in........restaurants_payment_update"
    data={}
    category=None
    try: 
        print "try"
        category = PaymentOptions.objects.get(id = request.REQUEST['id'])
        form=PaymentOptionsForm(instance=category)
    except:
        print "form.errors"
        form=PaymentOptionsForm()
    if request.method == "POST":
        if category:
            print "if_1"
            form=PaymentOptionsForm(request.POST,instance=category)
        else: 
            print "else_1"
            form=PaymentOptionsForm(request.POST)
        
        if form.is_valid():
            cat_form=form.save(commit=False)
            cat_form.created_by = cat_form.modified_by = request.user
            cat_form.status = 'P'
            cat_form.save()
            form=PaymentOptionsForm()  #.. that will show the empty form when 'save & another chosen
            data = {'form':form,'cat':category}
            append_data={'cat':cat_form,'edit_url':reverse('admin_portal_restaurants_payment_update'), 'label': 'Update Option'}
            return success_response_to_restaurant_module(append_data, data, template, REST_PAYMENT_MSG)
        else:
            data = {'form':form,'cat':category}
            return error_response(data, template, REST_PAYMENT_MSG)
    else:
        print "Get"
        data = {'form':form,'cat':category}
        return render_to_response(template, data, context_instance=RequestContext(request))
    
    
@admin_required
def restaurants_payment_delete(request):
    data=response_delete_category(request, PaymentOptions, REST_PAYMENT_MSG)
    #.... data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return HttpResponse(simplejson.dumps(data))





@admin_required
def restaurants_price(request, template='admin/portal/restaurants/pricing.html'):
    data={}
    try:
        message = Messages[request.GET['msg']]
    except:
        message = False
    RestaurantPriceFormsets=modelformset_factory(RestaurantPrice,extra=3,form=RestaurantPriceForm,max_num=3)    
    if request.method == 'POST':
        data['restaurant_price_forms']=restaurant_price_forms=RestaurantPriceFormsets(request.POST)
        if restaurant_price_forms.is_valid():
            restaurant_price_forms.save()
            messages.success(request, str(RESTAURANT_MSG['APS'])) 
            return HttpResponseRedirect(reverse('admin_portal_restaurants_price'))
        else:
            data['restaurant_price_forms'] = restaurant_price_forms
    else: 
        data['restaurant_price_forms']=RestaurantPriceFormsets()
    try:
        data['msg'] =RESTAURANT_MSG[request.GET['msg']]
    except:
        data['msg'] =False
    try:
        data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:
        data['mtype']=False
    return render_to_response(template, data, context_instance=RequestContext(request))





































    
    
