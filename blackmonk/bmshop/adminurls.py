from django.conf.urls import patterns,url,include

urlpatterns = patterns('',
                       
         url(r'^/?$','bmshop.shop.adminviews.admin_settings',name='admin_shop_home'),        
         url(r'^main/', include('bmshop.shop.adminurls')),
         url(r'^products/', include('bmshop.products.adminurls')),
 
     
) 