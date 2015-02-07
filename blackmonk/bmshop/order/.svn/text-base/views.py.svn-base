import random
import string
import datetime
import time
import stripe 

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect  
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings

from bmshop.order.forms import AddressForm
from bmshop.order.models import Order,OrderItem
from bmshop.order.utils import get_order_num
from bmshop.cart.utils import show_cart,get_cart
from bmshop.customer.models import Address
from bmshop.cart.models import Cart,CartItem
from bmshop.shop.models import PymentSettings,Shop
from common.models import PaymentConfigure
from bmshop.order.settings import *
from bmshop.mail_utils import send_mail_order,send_notify

from payments.utils import get_shop_paypal_form,get_invoice_num
from common.utils import get_global_settings
from payments.googlecheckout.models import GCNewOrderNotification
from payments.googlecheckout.views import GoogleCheckoutIntegration
from payments.authorizenet import AUTHNET_POST_URL, AUTHNET_TEST_POST_URL
from payments.authorizenet.forms import SIMPaymentForm,SIMBillingForm
from payments.authorizenet.utils import get_fingerprint
from payments.models import PaymentOrder

from common.utils import get_global_settings

@login_required
def check_out(request,cart_id=None,template='default/bmshop/check_out_address.html'):
    form = AddressForm()
    cart_obj = get_cart(request)

    if cart_id is not None:
        selected_cart = Cart.objects.get(id=cart_id)
        if cart_obj is None:
            selected_cart.user = request.user
            selected_cart.save()
        else:    
            for item in selected_cart.get_cart_items():
                try:
                    item_obj = CartItem.objects.get(cart_id = cart_obj.id,product_id=item.product.id)
                    item_obj.amount += item.amount
                    item_obj.save()
                except:
                    item.cart = cart_obj
                    item.save()
            selected_cart.delete()
    
    if request.method =='POST':
        form = form=AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return HttpResponseRedirect(reverse('bmshop_product_order_summery',args=[address.id]))
    
    try:seo = Shop.get_shop_settings()
    except:seo = None
    
    address_objs = Address.objects.filter(user=request.user).order_by('-id')
    data = {'form':form,
            'address_objs':address_objs,
            'seo':seo}
    return render_to_response (template, data, context_instance=RequestContext(request))

@login_required
def order_summery(request,address_id,template='bmshop/user/order_summery.html'):
    cart_check = get_cart(request)
    msgs = cart_check.validate_cart()
    payment_config = PaymentConfigure.get_payment_settings()
    pay_obj = PymentSettings.get_pay_settings()
    cart=show_cart(request)
    data = {'cart': cart,
            'address_id':address_id,
            'payment_config':payment_config,
            'pay_obj':pay_obj,
            'stripe_sp_cost':round(cart['cart_price']*100,0),
            'msgs':msgs}
    return render_to_response (template, data, context_instance=RequestContext(request))
    
@login_required
def remove_item(request, item_id):
    try:
        cart_item = CartItem.objects.get(pk=item_id)
        cart_item.delete()
    except:pass  
    addr_id = request.GET['aid']  
    return HttpResponseRedirect(reverse('bmshop_product_order_summery',args=[addr_id])) 
    
@login_required
def order_payment(request,template='bmshop/user/payment_submit.html'):
    global_settings=get_global_settings()
    
    if request.method =='POST':
        payment_settings=currency=PaymentConfigure.get_payment_settings()
        try:address_id = request.POST['shpng_addrs_id_stripe']
        except:address_id = request.POST['shpng_addrs_id']
        try:address = Address.objects.get(id=int(address_id))
        except:address = Address.objects.filter(user=request.user)[:1][0]
        cart = get_cart(request)
        
        if cart is None:return HttpResponseRedirect(reverse('bmshop_product_order_summery',args=[address_id]))
        
        order = Order(user=request.user)
        order.session = request.session.session_key
        order.order_number = get_order_num(8)
        order.status = SUBMITTED
        order.delivery_status = NOT_DELIVERED
        order.price = cart.get_total_price()
        order.tax = cart.get_total_tax()
        
        order.shipping_method = cart.get_shipping_method()
        order.shipping_price = cart.get_shipping_charge()
        
        order.name = address.firstname
        order.email = request.user.email
        order.address = address.address
        order.city = address.city
        order.state = address.state
        order.zip_code = address.zip_code
        order.country = address.country 
        order.phone = address.phone
        
        order.save()
        
        for cart_item in cart.get_cart_items():
            order_item = OrderItem.objects.create(
                order=order,
                price=cart_item.get_product_total_price(),
                quantity=cart_item.amount,
    
                product=cart_item.product,
                product_uid=cart_item.product.uid,
                product_name=cart_item.product.name,
                
                product_price=cart_item.product.for_sale_price,
            )
            cart_item.product.decrease_stock_amount(cart_item.amount)
        
        payment_config =currency= PaymentConfigure.get_payment_settings()
        pay_option=None
        data = {'pay_option':pay_option,'module':'dashboard','order':order}
        
        stripe_token = request.POST.get('stripeToken',False)
        if stripe_token:
            stripe.api_key = currency.stripe_private_key
            globalsettings=get_global_settings()
            try:
                charge = stripe.Charge.create(
                    amount=int(order.price*100), # amount in cents, again
                    currency=currency.currency_code,
                    card=stripe_token,
                    description="Items Order Id:"+order.order_number
                )
                
                order_obj=Order.objects.get(pk = order.id)
                order_obj.transaction_id = charge.id
                if not charge.paid:
                    order_obj.status = 4
                else:
                    order_obj.status = 1 
                    try:
                        cart = Cart.objects.get(user_id=order_obj.user.id)
                        cart.delete()
                    except:pass 
                    send_mail_order(order_obj)  

                order_obj.payment_method = 'ST'  
                order_obj.payment_price = float(order.price*100)
                order_obj.save()
                send_notify(order_obj)

                po=PaymentOrder(content_object=order_obj)
                po.invoice_no=get_invoice_num()
                po.transactionid=charge.id
                po.txn_type=''
                po.payment_mode='Stripe'
                if charge.paid:po.status='Success'
                else:po.status='Failed'  
                po.amount=float(order.price*100)
                if request.user.is_authenticated():po.user = request.user
                po.listing_type ="Shopping"
                po.object_name="Shopping"
                po.save()
                return HttpResponseRedirect("/user/shop/orders/?msg=REV&mtype=s")
            except:return HttpResponseRedirect(reverse('bmshop_product_home'))
        else:
            pay_option = request.POST['payment_option']
            if pay_option == 'paypal':
                form = get_shop_paypal_form("Shop Items",order.price,':'.join(['shop',str(order.id)]))
                data['form'] = form
            
            elif pay_option == 'google_checkout':
                
                object_id=str(order.id)
                invoice_id=str(get_invoice_num())
                user_id=str(request.user.id)
                
                globalsettings=get_global_settings()
                
                c_msg="shop:#"+object_id+':#'+invoice_id+':#'+user_id
                fields = {'items': [{'amount':order.price,
                                     'name': "Items Order Id:"+order.order_number,
                                     'description':'',
                                     'id': c_msg,
                                     'currency':payment_config.currency_code,
                                     'quantity': 1,
                                    }],
                          'return_url': "%s/user/shop/orders/?msg=REV&mtype=s"%(global_settings.website_url),}
                details={'merchant_id':str(payment_config.merchant_id),'merchant_key':str(payment_config.merchant_key)}
                google_checkout_obj=GoogleCheckoutIntegration(details)
                google_checkout_obj.add_fields(fields)
                data['gc_obj']= google_checkout_obj
                data['gc_payment_option']=google_checkout_obj.generate_cart_xml   
           
            elif pay_option == 'authorizenet':
                authorizenet_invoice=str(get_invoice_num())
                shop_obj = Shop.get_shop_settings()
                date = datetime.datetime.now()
                params = {
                    'custom': 'shop:'+str(order.id)+':'+str(request.user.id),
                    'x_amount': "%.2f" % float(order.price),
                    'x_fp_sequence': order.order_number,
                    'x_invoice_num': authorizenet_invoice,
                    'x_description': "Items Order Id:"+order.order_number ,
                    'x_currency_code':payment_config.currency_code,
                    'x_fp_timestamp': str(int(time.time())),
                    'x_receipt_link_url': global_settings.website_url+"/user/shop/orders/",
                    'x_relay_response':False,
                    }
                try:
                    billing_params = {'x_first_name': order.name,
                                      'x_last_name': '',
                                      'x_company': '',
                                      'x_address': order.address,
                                      'x_city': order.city,
                                      'x_state': order.state,
                                      'x_zip': order.zip_code,
                                      'x_country': shop_obj.get_default_country_display,
                                      'x_phone': order.phone,
                                      'x_fax': '',
                                      'x_email': order.email,
                                      'x_cust_id': request.user.id}
                    billing_form = SIMBillingForm(initial=billing_params)
                except:
                    billing_form = None
                
                params['x_fp_hash'] = get_fingerprint(order.order_number,params['x_fp_timestamp'],params['x_amount'])
                forms = SIMPaymentForm(initial=params)
                
                if settings.DEBUG:post_url = AUTHNET_TEST_POST_URL
                else:post_url = AUTHNET_POST_URL
                
                data['forms']=forms
                data['billing_form']=billing_form
                data['post_url']=post_url
                data['module']='shop'
            data['pay_option']=pay_option
            return render_to_response (template, data, context_instance=RequestContext(request))
    return HttpResponseRedirect(reverse('bmshop_product_home'))
    
    