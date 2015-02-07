from django.conf.urls import patterns,url,include

urlpatterns = patterns('',
         url(r'^products/', include('bmshop.products.staffurls')),
         url(r'^orders/', include('bmshop.order.staffurls')),
 
     
) 