from haystack.views import SearchView
from haystack.query import SearchQuerySet
from django.db import models

class SearchViewWithOrdering(SearchView):
    """ Override haystack SearchView to apply ordering to SearchQuerySet
        
        if parameter 'o' is in request and 'o' is in order_types the SearchQuerySet is reordered
        else the default order is 'score'
    
     """    
    __name__ = 'SearchViewWithOrdering'
    
    def __init__(self, *args, **kwargs):
        self.order_types = ['text','-text','pub_date','-pub_date', 'votes_score', '-votes_score']
        super(SearchViewWithOrdering, self).__init__(*args, **kwargs)
    
    def build_form(self, form_kwargs=None):
        if form_kwargs is None:
            form_kwargs = {}
        
        if self.searchqueryset is None:
            order = self.request.GET.get('o')
            sqs = SearchQuerySet().models(*self.get_models())

            if order in self.order_types:
                sqs = sqs.order_by(order)
            
            form_kwargs['searchqueryset'] = sqs
            
        return super(SearchViewWithOrdering, self).build_form(form_kwargs)


    def get_models(self):
        """Return an alphabetical list of model classes in the index."""
        search_models = []
        for model in self.request.GET.getlist('models'):
            search_models.append(models.get_model(*model.split('.')))
        return search_models
    
    def search(self):
        raise Exception('s')
        sqs = super(SearchViewWithOrdering, self).search()
        return sqs.models(*self.get_models())