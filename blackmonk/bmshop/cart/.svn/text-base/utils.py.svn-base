from django.conf import settings

from bmshop.cart.models import Cart
from bmshop.shop.models import Shop

def get_or_create_cart(request):
    cart = get_cart(request)
    if cart is None:
        cart = create_cart(request)

    return cart

def create_cart(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    cart = Cart(session=request.session.session_key)
    if request.user.is_authenticated():
        cart.user = request.user

    cart.save()
    return cart


def get_cart(request):
    session_key = request.session.session_key
    user = request.user

    if user.is_authenticated():
        try:
            cart = Cart.objects.get(user=user)
            return cart
        except:
            return None
    else:
        try:
            cart = Cart.objects.get(session=session_key)
            return cart
        except:
            return None
        

def show_cart(request):
    return_data = {}
    try:
        cart = get_cart(request)
        if cart is None:
            print cart
        elif not cart.get_cart_items():
            Msg="Your shopping bag is empty."
        else:
            Msg="Your shopping bag"
        
        shop = Shop.get_shop_settings()
        
        cart_base_price = cart.get_price()
        cart_shipping_charge = cart.get_shipping_charge() 
        cart_price = cart.get_total_price() 
        cart_tax = cart.get_total_tax() 
        cart_items = []
        count=0
        for cart_item in cart.get_cart_items():
            count+=1
            product = cart_item.product
            quantity = cart_item.amount
            cart_items.append({
                "properties" : cart_item.get_properties(),
                "obj": cart_item,
                "quantity": int(quantity),
                "product": product,
            })
        return_data = {
            "cart_items": cart_items,
            "cart_base_price": cart_base_price,
            "cart_shipping_charge":cart_shipping_charge,
            "cart_price": cart_price,
            "cart_tax": cart_tax,
            "cart_item_count":count,
            "Msg":Msg,
        }
    except:
        return_data['cart_item_count']=0
        return_data['Msg'] = "There is no item in your bag"
    return return_data
        