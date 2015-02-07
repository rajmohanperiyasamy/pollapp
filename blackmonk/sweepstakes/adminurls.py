from django.conf.urls import patterns, url

urlpatterns = patterns('sweepstakes.adminviews',
    url(r'^/?$', 'sweepstakes_settings', name='admin_portal_sweepstakes'),
    url(r'^settings/?$', 'sweepstakes_settings', name='admin_portal_sweepstakes_approval'),
    url(r'^qanda/?$', 'sweepstakes_qanda', name='admin_portal_sweepstakes_qanda'),
    url(r'^qanda-update/?$', 'sweepstakes_qanda_update', name='admin_portal_sweepstakes_qanda_update'),
    url(r'^qanda-delete/?$', 'sweepstakes_qanda_delete', name='admin_portal_sweepstakes_qanda_delete'),
)
