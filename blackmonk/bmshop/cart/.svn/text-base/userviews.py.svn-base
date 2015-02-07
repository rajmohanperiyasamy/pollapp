from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils import simplejson  

from bmshop.static_msgs import USER_MSG
from bmshop.products.models import Product
from bmshop.cart import utils as cart_utils




def add_to_cart(request):
    try:
        product = Product.objects.get(pk=request.GET['id'])
        cart = cart_utils.get_or_create_cart(request)
        
        cart_it = cart.add(product, 1)
        status = cart_it[2]
        cart_item = cart_it[0]
        msg = cart_it[1]
        cart_items = [cart_item]
        
        request.session["cart_items"] = cart_items
        request.session["cart_msg"] = msg
        request.session['status'] = status
        data = {'status':status,'msg':msg}
    except:
        data = {'status':False,'msg':str(USER_MSG['OOPS'])}    
    return HttpResponse(simplejson.dumps(data))
    
    
    