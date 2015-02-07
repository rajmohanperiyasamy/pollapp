from django.conf.urls import patterns, url

urlpatterns = patterns(
    'api.views',
    url(r'^tasks/$', 'task_list', name='task_list'),
    url(r'^tasks/(?P<pk>[0-9]+)$', 'task_detail', name='task_detail'),
    url(r'^add_task/$', 'add_task', name='add_task'),
    url(r'^add_employee/$', 'add_employee', name='add_employee'),
)