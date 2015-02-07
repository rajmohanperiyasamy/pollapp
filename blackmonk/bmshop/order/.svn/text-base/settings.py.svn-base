from django.utils.translation import ugettext_lazy as _

SUBMITTED = 0
PAID = 1
CANCELED = 2
PAYMENT_FAILED = 3
PENDING = 4

ORDER_STATES = [
    (SUBMITTED, _(u"Not Paid")),
    (PAID, _(u"Paid")),
    (CANCELED, _(u"Canceled")),
    (PAYMENT_FAILED, _(u"Payment Failed")),
    (PENDING, _(u"Pending")),
]


NOT_PAID = 'NT'
PAYPAL = 'PP'
GOOGLE_CHK_OUT = 'GC'
AUTHRIZENET = 'AN'
STRIPE = 'ST'

PAYMENT_MODE = [
    (NOT_PAID, _(u" -- ")),
    (PAYPAL, _(u"Paypal")),
    (GOOGLE_CHK_OUT, _(u"Google Checkout")),
    (AUTHRIZENET, _(u"Authorizenet")),
    (STRIPE,_(u'Stripe'))
]

NOT_DELIVERED = 'N'
SHIPPED = 'S'
DELIVERED = 'D'

DELIVERY_STATUS = [
    (NOT_DELIVERED, _(u"Pending")),
    (SHIPPED, _(u"Shipped")),
    (DELIVERED, _(u"Delivered")),
]