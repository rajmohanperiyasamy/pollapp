from django.conf.urls import patterns, url

urlpatterns = patterns('meetup.adminviews',
    url(r'^/?$', 'meetup_settings', name='admin_portal_meetup'),
    url(r'^settings/?$', 'meetup_settings', name='admin_portal_meetup_settings'),
    url(r'^validate-api/?$', 'validate_meetup_api', name='admin_validate_meetup_api'),
)