from django import template


register = template.Library()

@register.filter  
def get_banner_clicks_mnthly(month,banner):   
    from banners.models import BannerAdvertisements, BannerReports
    try:
        banner = BannerAdvertisements.objects.get(id = banner)
        clicks=BannerReports.objects.filter(banner = banner, is_clicked = True, viewed_on__month = month.month, viewed_on__year = month.year).count()
        return clicks
    except:
        return 0
    
@register.filter
def to_class_name(value):
    return value.__class__.__name__