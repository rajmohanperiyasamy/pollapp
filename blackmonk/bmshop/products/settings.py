from django.utils.translation import ugettext_lazy as _


DELIVERY_TIME_UNIT_HOURS = 1
DELIVERY_TIME_UNIT_DAYS = 2
DELIVERY_TIME_UNIT_WEEKS = 3
DELIVERY_TIME_UNIT_MONTHS = 4

DELIVERY_TIME_UNIT_CHOICES = (
    (DELIVERY_TIME_UNIT_HOURS, _(u"hours")),
    (DELIVERY_TIME_UNIT_DAYS, _(u"days")),
    (DELIVERY_TIME_UNIT_WEEKS, _(u"weeks")),
    (DELIVERY_TIME_UNIT_MONTHS, _(u"months")),
)
PROPERTY_TEXT_FIELD = 1
PROPERTY_SELECT_FIELD = 2
PROPERTY_NUMBER_FIELD = 3
PROPERTY_FIELD_CHOICES = (
    (PROPERTY_TEXT_FIELD, _(u"Text field")),
    (PROPERTY_SELECT_FIELD, _(u"Select field")),
    (PROPERTY_NUMBER_FIELD, _(u"Number field")),
    
)
PROPERTY_DISPLAYBLE = 1
PROPERTY_FILTERIBLE = 2