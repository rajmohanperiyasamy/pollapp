from django.conf.urls import *

urlpatterns = patterns('jobs.views',
            
            url(r'^/?$', 'category_list', name='jobs_category_list'),
            url(r'^all/$', 'job_list', name='jobs_job_list'),
            url(r'^attsearch/(?P<slug>[-\w]+)\/?$', 'attribute_search', name='jobs_attribute_search'),
            url(r'^search/$', 'search_job', name='jobs_search_job'),
)

