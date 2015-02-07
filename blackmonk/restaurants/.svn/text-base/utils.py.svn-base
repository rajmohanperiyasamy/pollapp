

from restaurants.models import RestaurantTags, RestaurantCategories, RestaurantLogo

def save_restaurant_tags(taglist,restaurant):
    try:taglist = taglist.split(',')
    except:taglist = taglist
    restaurant.tags.clear()
    for nt in taglist:
        if nt!='':
            try:tag_obj = RestaurantTags.objects.get(tag__iexact = nt)
            except:
                tag_obj = RestaurantTags(tag = nt) 
                tag_obj.save()
            restaurant.tags.add(tag_obj)       
    

        
def save_restaurant_logo(logoid, restaurant):
    logo_obj = RestaurantLogo.objects.get(id=logoid)
    restaurant.logo = logo_obj
    restaurant.save()