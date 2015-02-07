import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from bmshop.static_msgs import USER_MSG
from common.templatetags.ds_utils import get_msg_class_name
from bmshop.products.models import Product
from bmshop.customer.models import Wishlist

@login_required
def wishlist(request,template='bmshop/user/wishlist.html'):
    wishlists=Wishlist.objects.filter(added_by_id=request.user.id).order_by('-id')
    products=[]
    for wishlist in wishlists:
        try:
            product = Product.objects.get(pk=wishlist.products_id)
            products.append(product)
        except:pass
        
    data = {'products':products}
    try:data['msg'] =USER_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    return render_to_response (template, data, context_instance=RequestContext(request))

@login_required
def add_wishlist(request,slug):
    if request.user.is_authenticated():
        user_id = request.user.id
    date = datetime.datetime.now()
    product = Product.objects.get(slug=slug)
    wishlists=Wishlist.objects.filter(products_id=product.id,added_by_id=user_id)
    if not wishlists:
        wishlist_data=Wishlist(added_on=date,products_id=product.id,added_by_id=user_id)
        wishlist_data.save()
        request.session['wishlist_message'] = "Added to wish list"
        url=product.get_absolute_url()
        return HttpResponseRedirect(url)
    else:
        wishlists.delete()
        request.session['wishlist_message'] = "Add to wish list"
        url=product.get_absolute_url()
        return HttpResponseRedirect(url)
    
@login_required
def delete_wishlist(request):
    try:
        product = Product.objects.get(id=request.GET['id'])
        wishlists=Wishlist.objects.filter(products_id=product.id,added_by_id=request.user.id)
        wishlists.delete()
        data = {'msg':str(USER_MSG['WDS']),'status':1}
    except:
        data = {'msg':str(USER_MSG['OOPS']),'status':0}
    return HttpResponse(simplejson.dumps(data))
    
    
    