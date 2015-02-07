from django.conf.urls import patterns, url

urlpatterns = patterns('jobs.adminviews',
    
    url(r'^/?$', 'jobs_settings', name='admin_portal_jobs'),
    url(r'^settings/?$', 'jobs_settings', name='admin_portal_jobs_settings'),
    url(r'^validate-api/?$', 'validate_jobs_api', name='admin_validate_jobs_api'),
)