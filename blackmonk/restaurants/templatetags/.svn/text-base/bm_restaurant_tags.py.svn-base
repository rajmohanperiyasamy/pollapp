from django.template import Library
from restaurants.models import Restaurants, Cuisines, RestaurantCategories, RestaurantFeatures, MealTypes

register = Library()

GET_PRICE_RANGE_FORMAT = {25:'$', 50:'$$', 75:'$$$', 100:'$$$$', 125:'$$$$'}

@register.assignment_tag
def get_featured_restaurants(**kwargs):
    limit = kwargs.get('limit', 20)
    cuisine = kwargs.get('cuisine', False)
    if cuisine:restaurants = Restaurants.objects.only('name','slug','ratings','logo').filter(cuisines = cuisine, status='P', featured_sponsored='F').select_related('logo').order_by('-id')[:limit] 
    else:restaurants = Restaurants.objects.only('name','slug','ratings','logo').filter(status='P', featured_sponsored='F').select_related('logo').order_by('-id')[:limit]
    return restaurants

@register.assignment_tag
def get_restaurants_cuisines():
    return Cuisines.objects.only('name','slug').order_by('name')

@register.assignment_tag
def get_restaurants_categories():
    return RestaurantCategories.objects.only('name','slug').order_by('name')

@register.assignment_tag
def get_restaurants_features():
    return RestaurantFeatures.objects.only('name').order_by('name')

@register.assignment_tag
def get_restaurants_meal_types():
    return MealTypes.objects.only('name').order_by('name')

@register.filter
def get_price_range_fmt(price):
    try:return GET_PRICE_RANGE_FORMAT[price]
    except:price