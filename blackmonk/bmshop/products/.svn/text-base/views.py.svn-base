from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.db.models import Max,Min
from django.db.models import Q

from bmshop.products.models import Category,Product,Manufacturer,ProductPropertyValue,BMProperty
from bmshop.products.settings import PROPERTY_DISPLAYBLE,PROPERTY_SELECT_FIELD
from bmshop.shop.models import Shop
from bmshop.cart.utils import show_cart
from bmshop.customer.models import Wishlist
from bmshop.products.utils import get_manufactures,get_sort,get_price_filter,get_cat_manufacture
from common.utils import ds_pagination

NO_OF_ITEMS_PER_PAGE = 16

def home(request,template='default/bmshop/home.html'):
    
    category_objs=Category.objects.filter(parent=None,featured=True).order_by('position') 
    
    try:seo = Shop.get_shop_settings()
    except:seo = None
    
    data = {
            'category_objs': category_objs,
            'cart': show_cart(request),
            'main_cats': Category.objects.filter(parent=None).order_by('position'), 
            'seo': seo
            }
    return render_to_response (template, data, context_instance=RequestContext(request))

def product_category_list(request,catslug,parent_slug=None,template='default/bmshop/category_listing.html'):
    product_objs = None
    price_options = None
    property_objs = None
    has_next = None
    product_count = None
    
    cat_obj=Category.objects.get(slug=catslug)
    
    if cat_obj.is_leaf_node():
        template='default/bmshop/product_filter.html'
        args = filter_products(request,cat_obj)
        product_objs = args['product_objs']
        price_options = args['price_options']
        property_objs = args['property_objs']
        has_next = args['has_next'] 
        product_count = args['count']
    data = {
        'cat_obj': cat_obj,
        'product_objs': product_objs,
        'cart': show_cart(request),
        'price_options': price_options,
        'manufactures': get_manufactures(cat_obj.slug),
        'main_cats': Category.objects.filter(parent=None).order_by('position'),
        'property_objs':property_objs,
        'has_next':has_next,
        'product_count':product_count
        }
    
    return render_to_response (template, data, context_instance=RequestContext(request))

def _get_filter_properties(products):
    property_ids = []
    for product in products:
        pty_values = ProductPropertyValue.objects.filter(product_id=product.id).distinct('property__id')
        for pt_val in pty_values:
            if pt_val.property.filterable:
                property_ids.append(pt_val.property.id)
        
        
    properties  = BMProperty.objects.filter(pk__in=property_ids)
    return properties 

def _get_property_products(property_ids,cat_ids):
    prdct_ids = []
    pty_values = ProductPropertyValue.objects.filter(property_id__in=property_ids)
    for pty_val in pty_values:
        prdct_ids.append(pty_val.product.id)
        
    return prdct_ids
    
def ajax_filter_products(request,template='default/bmshop/include_product_filter.html'):
    data = filter_products(request)
    html = render_to_string(template,data,context_instance=RequestContext(request))
    send_data={'html':html,
               'product_count':data['count'],
               'page':data['page'],
               'has_next':data['has_next']
               }
    return HttpResponse(simplejson.dumps(send_data))

def filter_products(request,main_cat=None):
    price_options = None
    property_objs = None
    key = {'status':'P'}
    product_ids = []
    
    page = request.GET.get('page',False)
    if page:page = int(page)+1
    else:page = 1
    
    manufacture_ids=request.GET.get('manufacture',None)
    if manufacture_ids:
        manufacture_ids = manufacture_ids.split(',')
        if u'' in manufacture_ids: manufacture_ids.remove(u'')  
    
    property_ids=request.GET.get('property',None)
    if property_ids:
        property_ids = property_ids.split(',')
        if u'' in property_ids: property_ids.remove(u'')
    
    if main_cat is None:
        cat_ids = request.GET['cat_id'].split(',')
        if u'' in cat_ids: cat_ids.remove(u'')  
        
        if cat_ids:    
            key['categories__in'] = cat_ids
    else:
        key['categories'] = main_cat
        
    sort = get_sort(request.GET.get('sort','default'))
    search_kwd = request.GET.get('search_query',None)
    
    if manufacture_ids:
        key['manufacturer__in'] = manufacture_ids
    
    price_values=request.GET.get('price_range',None)
    if price_values:
        price_values = price_values.split(',')
        if u'' in price_values: price_values.remove(u'')  
    
    if property_ids:
        feature_ids = _get_property_products(property_ids,cat_ids)
    
    if price_values:
        range_ids = []
        for price in price_values: 
            value = price.split('-')
            min = value[0]
            max = value[1]
            if property_ids:
                products = Product.objects.filter(status="P",for_sale_price__range=(min, max),categories__in=cat_ids,pk__in=feature_ids)
            else:
                products = Product.objects.filter(status="P",for_sale_price__range=(min, max),categories__in=cat_ids)    
            for product in products:
                range_ids.append(product.id)
    
    if property_ids and price_values:
        product_ids = range_ids
    elif property_ids:
        product_ids = feature_ids
    elif price_values:
        product_ids = range_ids
            
    if search_kwd:
        q =(Q(name__icontains=search_kwd)|Q(categories__name__icontains=search_kwd)|Q(manufacturer__name__icontains=search_kwd))
        product_objs = Product.objects.filter(q,**key).order_by(sort)
    else:
        if property_ids or price_values:
            product_objs = Product.objects.filter(pk__in=product_ids,**key).order_by(sort)
        else:  
            product_objs = Product.objects.filter(**key).order_by(sort)
    
    if main_cat:
        if product_objs:
            price_options = get_price_filter(request,product_objs)
        property_objs = _get_filter_properties(product_objs)
    
    
    data = ds_pagination(product_objs,page,'product_objs',NO_OF_ITEMS_PER_PAGE)
    
    data['product_count'] = product_objs.count()
    data['price_options'] = price_options
    data['property_objs'] = property_objs
    data['page'] = page
    return data

def search(request,template='default/bmshop/search_result.html'):
    try:seo = Shop.get_shop_settings()
    except:seo = None
    
    key = {'status':'P'}
    manufactures = None
    cat_ids = []
    try:
        cat_obj = Category.objects.get(id=request.GET['cat'])
        for cat in cat_obj.get_all_children():
            cat_ids.append(cat.id)
        
    except:
        cat_obj = None
    
    if cat_ids:
        key['categories__id__in'] = cat_ids
    
    query = request.GET['query']
    
    if query:
        q =(Q(name__icontains=query)|Q(categories__name__icontains=query)|Q(manufacturer__name__icontains=query))
        product_objs = Product.objects.filter(q,**key).order_by('-created_on').distinct()
    else:
        product_objs = Product.objects.filter(**key).order_by('-created_on').distinct()
        
    cat_objs,man_objs = get_cat_manufacture(product_objs)    

    data = {
            'query':query,
            'cat_objs':cat_objs,
            'man_objs':man_objs,
            'cart': show_cart(request),
            'product_objs':product_objs,
            'manufactures':manufactures,
            'main_cats': Category.objects.filter(parent=None).order_by('position'),
            'seo':seo  
            }
    return render_to_response (template, data, context_instance=RequestContext(request))
    

def get_properties(request,product_obj):
    displayables = []
    is_displayables = False
    
    for group_obj in product_obj.property_groups.all().order_by('position'):
        properties = []
        for property in group_obj.properties.filter(display_on_product=True).order_by("bmgroupsproperties"):
            is_displayables = True

            ppvs = ProductPropertyValue.objects.filter(property=property,group=group_obj,product=product_obj, type=PROPERTY_DISPLAYBLE)
            value_ids = [ppv.value for ppv in ppvs]

            select_options = []
            for option in property.options.all():
                if str(option.id) in value_ids: 
                    select_options.append(option.name)
            
            value = ""
            if property.type == PROPERTY_SELECT_FIELD:
                display_select_field = True
            else:
                display_select_field = False
                try:
                    value = value_ids[0]
                except IndexError:pass

            properties.append({"id": property.id,"name": property.name,"title": property.title,
                 "type": property.type,"select_options": select_options,"value": value,
                "display_text_field": not display_select_field,"display_select_field": display_select_field, })
       
        displayables.append({"id": group_obj.id, "name": group_obj.name, "properties": properties, })
        
    return displayables

def product_detail(request,slug,template='default/bmshop/product_detail.html'):
    
    product_obj = Product.objects.get(slug=slug)
    
    display_properties = get_properties(request,product_obj)
    
    accrssories_objs = Product.objects.filter(id__in=product_obj.get_accessories()).order_by('-featured')[:4]
    
    related_objs = Product.objects.filter(id__in=product_obj.related_products.all(),status='P').order_by('-featured')
    
    if not related_objs:
        related_objs = Product.objects.filter(manufacturer__id = product_obj.manufacturer.id,categories__in=product_obj.categories.all(),status='P').exclude(id=product_obj.id).order_by('-featured')[:5]
    
    wishlist = Wishlist.objects.filter(added_by = request.user.id,products_id = product_obj.id)
    
    if wishlist:message = "Added to wishlist"
    else:message = "Add to wishlist"  
            
    data = {'product_obj':product_obj,
            'display_properties':display_properties,
            'accrssories_objs':accrssories_objs,
            'related_objs':related_objs,
            'cart':show_cart(request),
            'message':message}
    main_cats=Category.objects.filter(parent=None).order_by('position') 
    data['main_cats'] = main_cats
    return render_to_response (template, data, context_instance=RequestContext(request))



