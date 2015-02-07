from __future__ import unicode_literals
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from haystack.forms import ModelSearchForm, FacetedSearchForm,SearchForm
from haystack.query import EmptySearchQuerySet
from common.utils import ds_pagination

RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 10)


class SearchView(object):
    template = 'search/search.html'
    extra_context = {}
    query = ''
    results = EmptySearchQuerySet()
    request = None
    form = None
    results_per_page = RESULTS_PER_PAGE

    def __init__(self, template=None, load_all=True, form_class=None, searchqueryset=None, context_class=RequestContext, results_per_page=None):
        self.load_all = load_all
        self.form_class = form_class
        self.context_class = context_class
        self.searchqueryset = searchqueryset
        if form_class is None:
            self.form_class = SearchForm

        if not results_per_page is None:
            self.results_per_page = results_per_page

        if template:
            self.template = template

    def __call__(self, request):
        """
        Generates the actual response to the search.

        Relies on internal, overridable methods to construct the response.
        """
        self.request = request

        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results()

        return self.create_response()

    def build_form(self, form_kwargs=None):
        """
        Instantiates the form the class should use to process the search query.
        """
        data = None
        kwargs = {
            'load_all': self.load_all,
        }
        if form_kwargs:
            kwargs.update(form_kwargs)

        if len(self.request.GET):
            data = self.request.GET

        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = self.searchqueryset

        return self.form_class(data, **kwargs)

    def get_query(self):
        """
        Returns the query provided by the user.

        Returns an empty string if the query is invalid.
        """
        if self.form.is_valid():
            return self.form.cleaned_data['q']

        return ''

    def get_results(self):
        """
        Fetches the results via the form.

        Returns an empty list if there's no query to search with.
        """
        return self.form.search()

    def build_page(self):
        """
        Paginates the results appropriately.

        In case someone does not want to use Django's built-in pagination, it
        should be a simple matter to override this method to do what they would
        like.
        """
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        #start_offset = (page_no - 1) * self.results_per_page
        #self.results[start_offset:start_offset + self.results_per_page]
        self.results=self.results.exclude(django_ct='usermgmt.bmuser')[:2000]
        """
        data_counts={}
        if self.form_class == SearchForm:
            results_counts = [result.app_label for result in self.results]
            data_counts = {
                'articles': results_counts.count('article'),
                'classifieds': results_counts.count('classifieds'),
                'business': results_counts.count('business'),
                'events': results_counts.count('events'),
                'attractions': results_counts.count('attractions'),
                'videos': results_counts.count('videos'),
                'photos': results_counts.count('gallery'),
                'movies': results_counts.count('movies'),
                #'forum': results_counts.count('forum'),
                'bookmarks': results_counts.count('bookmarks'),
            }
        """
        data = ds_pagination(self.results,page_no,'results',self.results_per_page)
        #data.update(data_counts)
        return data

    def extra_context(self):
        """
        Allows the addition of more context variables as needed.

        Must return a dictionary.
        """
    
        models=''
        module=''
        try:
            models=self.form.cleaned_data['models']
            base_url='/search/ajax/?q='+self.query+'&models='+models[0]
        except:
            base_url='/search/?q='+self.query
        try:module=models[0].split('.')[1]
        except:pass
        return {'baseurl':base_url,'models':models,'module':module}

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        data = self.build_page()

        context = {
            'query': self.query,
            'form': self.form,
            'suggestion': None,
        }
        context.update(data)
        if not self.results and hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            suggestion= self.form.get_suggestion()
            if suggestion and suggestion.strip():
                context['suggestion']=suggestion
        context.update(self.extra_context())
        return render_to_response(self.template, context, context_instance=self.context_class(self.request))


def search_view_factory(view_class=SearchView, *args, **kwargs):
    def search_view(request):
        return view_class(*args, **kwargs)(request)
    return search_view


class FacetedSearchView(SearchView):
    __name__ = 'FacetedSearchView'

    def __init__(self, *args, **kwargs):
        # Needed to switch out the default form class.
        if kwargs.get('form_class') is None:
            kwargs['form_class'] = FacetedSearchForm

        super(FacetedSearchView, self).__init__(*args, **kwargs)

    def build_form(self, form_kwargs=None):
        if form_kwargs is None:
            form_kwargs = {}

        # This way the form can always receive a list containing zero or more
        # facet expressions:
        form_kwargs['selected_facets'] = self.request.GET.getlist("selected_facets")

        return super(FacetedSearchView, self).build_form(form_kwargs)

    def extra_context(self):
        extra = super(FacetedSearchView, self).extra_context()
        extra['request'] = self.request
        extra['facets'] = self.results.facet_counts()
        return extra


def basic_search(request, template='search/search.html', load_all=True, form_class=ModelSearchForm, searchqueryset=None, context_class=RequestContext, extra_context=None, results_per_page=None):
    """
    A more traditional view that also demonstrate an alternative
    way to use Haystack.

    Useful as an example of for basing heavily custom views off of.

    Also has the benefit of thread-safety, which the ``SearchView`` class may
    not be.

    Template:: ``search/search.html``
    Context::
        * form
          An instance of the ``form_class``. (default: ``ModelSearchForm``)
        * page
          The current page of search results.
        * paginator
          A paginator instance for the results.
        * query
          The query received by the form.
    """
    query = ''
    results = EmptySearchQuerySet()

    if request.GET.get('q'):
        form = form_class(request.GET, searchqueryset=searchqueryset, load_all=load_all)

        if form.is_valid():
            query = form.cleaned_data['q']
            results = form.search()
    else:
        form = form_class(searchqueryset=searchqueryset, load_all=load_all)

    paginator = Paginator(results, results_per_page or RESULTS_PER_PAGE)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")

    context = {
        'form': form,
        'page': page,
        'paginator': paginator,
        'query': query,
        'suggestion': None,
    }

    if results.query.backend.include_spelling:
        context['suggestion'] = form.get_suggestion()

    if extra_context:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=context_class(request))
