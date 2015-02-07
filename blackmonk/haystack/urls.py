from __future__ import unicode_literals

from django.conf.urls import patterns, url

from haystack.views import SearchView
from haystack.forms import ModelSearchForm

urlpatterns = patterns('haystack.views',
    url(r'^$', SearchView(), name='haystack_search'),
    url(r'^ajax/?$', SearchView(form_class=ModelSearchForm,template="search/ajax_search_result.html"), name='haystack_model_search'),
)