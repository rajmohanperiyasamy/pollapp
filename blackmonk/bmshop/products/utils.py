import math
from random import choice
from django.db.models import Max,Min

from bmshop.products.models import Product,Category,Manufacturer



def get_product_key(cat=None):
    size=8
    if cat:
        name = cat[:3].strip()
        name = name.upper()
    while True:
        tid = ''.join([choice('ABCDEFGHKLNPRSTUWX345679') for i in range(size)])
        if cat:
            tid = name+tid 
        try:
            Product.objects.only('id').get(uid=tid)
        except:
            return tid


def get_manufactures(slug):
    try:
        category = Category.objects.get(slug = slug)
        brands = []
        products = category.products.all()
        for pro in products:
            try:
                manufacturer = Manufacturer.objects.get(id = pro.manufacturer.id)
                brands.append(manufacturer)
            except:pass
        brands = list(set(brands))
        if brands:
            brands = brands
        else:       
            brands = False
    except:
        brands = False
    return brands

def get_sort(sort):
    if "default" in sort:
        condition="-created_on"
    if "a_to_z" in sort:
        condition="name"
    if "z_to_a" in sort:
        condition="-name"
    if "low_to_high" in sort:
        condition="for_sale_price"
    if "high_to_low" in sort:
        condition="-for_sale_price"
    return condition

def roundup(x,range=1000):
    if range > 1000:
        range = 5000
    return int(math.ceil(x / float(range))) * int(range)

def get_price_filter(request,product_objs):
    
    price_filter = product_objs.aggregate(min_val=Min('for_sale_price'),max_val=Max('for_sale_price'))
    
    all_products = []
    for product in product_objs:
        all_products.append(product.id)
        
    pmin = price_filter["min_val"]
    pmax = price_filter["max_val"]
    
    if pmax == pmin:
        step = pmax
    else:
        diff = pmax - pmin
        step = diff / 3
    
    
    if step >= 0 and step < 3:
        step = 3
    elif step >= 3 and step < 6:
        step = 5
    elif step >= 6 and step < 11:
        step = 10
    elif step >= 11 and step < 51:
        step = 50
    elif step >= 51 and step < 101:
        step = 100
    elif step >= 101 and step < 501:
        step = 500
    elif step >= 501 and step < 1001:
        step = 1000
    elif step >= 1000 and step < 5001:
        step = 500
    elif step >= 5001 and step < 10001:
        step = 1000
    
    step = int(step)
    result = []
    for n, i in enumerate(range(0, int(pmax), step)):
        if i > pmax:
            break
        min = roundup(i,step) + 1
        static_max = i + step
        max = roundup(static_max,step)
       
        products = Product.objects.filter(for_sale_price__range=(min, max), pk__in=all_products)
        result.append({
            "min": min,
            "max": max,
            "quantity": len(products),
        })
    #return result
    new_result = []
    for n, f in enumerate(result):
        if f["quantity"] == 0:
            try:
                result[n + 1]["min"] = f["min"]
            except IndexError:
                pass
            continue
        new_result.append(f)

    return new_result


def get_cat_manufacture(products):
    cats = []
    product_ids = []
    man_ids = []
    for product in products:
        product_ids.append(product.id)
        man_ids.append(product.manufacturer.id)
        for cat in  product.categories.all():
            cats.append(cat.id)
    
    categories_objs = Category.objects.filter(pk__in=cats).distinct()
    cat_objs = []
    for cat in categories_objs:
        product = Product.objects.filter(categories__id = cat.id,pk__in=product_ids).count()
        cat_objs.append({'name':cat.name,
                    'product_count':product,
                    'cat':cat})    
    
    man_objs = Manufacturer.objects.filter(pk__in = man_ids)
        
    return cat_objs,man_objs    
    

