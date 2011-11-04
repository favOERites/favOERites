from django.conf.urls.defaults import *
from haystack_views import SearchViewWithOrdering
from haystack.forms import ModelSearchForm, SearchForm
    
urlpatterns = patterns('haystack.views',
    url(r'^$', SearchViewWithOrdering(form_class=SearchForm, results_per_page=20), name='haystack_search'),
)



