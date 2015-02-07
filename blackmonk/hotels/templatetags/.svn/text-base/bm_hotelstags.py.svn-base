from django.template import Library
from hotels.models import ApiSettings as HotelApiSettings
register = Library()

@register.assignment_tag
def get_expedia_api():
    try:
        expedia_api = HotelApiSettings.objects.all()[:1][0]
    except:
        expedia_api = None
    return expedia_api
