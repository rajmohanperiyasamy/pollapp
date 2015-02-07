import getsettings

from common.models import AvailableApps,AvailableModules

def process_menuitems():
    for app in AvailableApps.objects.all():
        slug='/'+app.slug+'/'
        menus=AvailableModules.objects.filter(base_url__icontains=slug)
        if app.status=='A':menus.update(is_active=True)
        else:menus.update(is_active=False)
    return True

process_menuitems()