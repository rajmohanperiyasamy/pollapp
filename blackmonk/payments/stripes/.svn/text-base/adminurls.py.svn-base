from django.conf.urls import patterns, url
urlpatterns = patterns('payments.stripes.adminviews',
    url(r'^add_subscription_plan/', 'stripe_add_plan',name="stripe_add_plan"),
    url(r'^subscription_plans/', 'stripe_list_plans',name="stripe_list_plans"),
    url(r'^stripe/plans/details/(?P<id>\d+)/', 'stripe_plan_details',name="stripe_plan_details"),
)
