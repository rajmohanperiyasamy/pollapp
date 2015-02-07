from django.conf.urls import patterns,url

urlpatterns = patterns('analytics.staffviews',
   url(r'^/?$','analytic',name='staff_analytic_home'),
   url(r'^extra/$','analytic_extra',name='staff_analytic_extra'),
   url(r'^live/$','analytic_live',name='staff_analytic_live'),
)

                            