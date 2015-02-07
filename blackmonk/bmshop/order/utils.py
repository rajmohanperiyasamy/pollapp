from random import choice

from bmshop.order.models import Order


def get_order_num(size=6):
    while True:
        tid = ''.join([choice('ABCDEFGHKLNPRSTUWX345679') for i in range(size)])
        tid = 'SHP%s'%(tid)
        try:
            Order.objects.only('id').get(order_number=tid)
        except:
            return tid