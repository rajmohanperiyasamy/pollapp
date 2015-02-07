from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect  
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from bmshop.static_msgs import USER_MSG
from bmshop.cart.models import Cart,CartItem,CartItemPropertyValue
from bmshop.products.models import Product
from bmshop.shop.models import Shop
from bmshop.cart import utils as cart_utils
from common.templatetags.currency import moneyfmt

def cart_view(request,template='default/bmshop/cart.html'):
    cart = cart_utils.show_cart(request)
    
    if request.method == 'POST':
        crt = cart_utils.get_cart(request)
        if crt is not None:
            if not crt.user:
                return HttpResponseRedirect(reverse('bmshop_product_check_out_with_cart',args=[crt.id]))
            else:
                return HttpResponseRedirect(reverse('bmshop_product_check_out'))
    
    try:seo = Shop.get_shop_settings()
    except:seo = None
            
    data = {'cart':cart,'seo':seo}
    return render_to_response (template, data, context_instance=RequestContext(request))

def add_cart(request,template='default/bmshop/lb_include_cart.html'):
    product = Product.objects.get(pk=request.POST['pid'])
    quantity = int(request.POST['quantity'])
    if product.manage_stock_amount:
        stock = product.stock_amount
        quantity = quantity
        if quantity > product.stock_amount:
            msg="Sorry there are only "+stock+" stock of "+product.name+"available"
            quantity = product.stock_amount
    
    cart = cart_utils.get_or_create_cart(request)
    cart_items=cart.get_cart_items()
    
    cart_it = cart.add(product, quantity)
    status = cart_it[2]
    cart_item = cart_it[0]
    msg = cart_it[1]
    cart_items = [cart_item]
    
    request.session["cart_items"] = cart_items
    request.session["msg"] = msg
    request.session['status'] = status
    
    if request.user.is_authenticated():
        request.session['cart'] = ""
    else:
        request.session['cart'] = cart
    
    cart = cart_utils.show_cart(request)
    html = render_to_string(template,{'cart':cart},context_instance=RequestContext(request))
    data = {'html':html,'cart_count':cart['cart_item_count'],'status':status,'msg':msg}
    
    return HttpResponse(simplejson.dumps(data))
       

def update_quantity(request):
    try:
        product = Product.objects.get(pk=request.GET['id'])
        quantity = float(request.GET['value'])
        
        cart = cart_utils.get_or_create_cart(request)
        cart_it = cart.add_update(product, quantity)
        status = cart_it[2]
        cart_item = cart_it[0]
        msg = cart_it[1]
        cart_items = [cart_item]
        amount=cart_item.amount
        cart = cart_utils.show_cart(request)
        
        item_price=moneyfmt(round(cart_item.get_product_total_price(),0))
        base_price=moneyfmt(round(cart['cart_base_price'],0))
        tax_price=moneyfmt(round(cart['cart_tax'],2))
        total_price=moneyfmt(round(cart['cart_price'],0))
        data = {'amount':amount,'status':status,'msg':msg,'val':int(cart_item.amount),'item_price':item_price,'base_price':base_price,'tax_price':tax_price,'total_price':total_price}
    except:
        data = {'status':False,'msg':str(USER_MSG['OOPS'])}    
    return HttpResponse(simplejson.dumps(data))
    
    
def remove_cart_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(pk=item_id)
        cart_item.delete()
    except:pass    
    return HttpResponseRedirect(reverse('bmshop_product_cart'))
