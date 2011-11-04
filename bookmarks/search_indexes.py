import datetime
from haystack.indexes import *
from haystack import site
from models import Bookmark, Playlist


class BookmarkIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(model_attr='user')
    pub_date = DateTimeField(model_attr='created')
    votes_score = IntegerField(model_attr='score')
    

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Bookmark.objects.filter()  
    
class PlaylistIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(model_attr='user')
    pub_date = DateTimeField(model_attr='created')
    votes_score = IntegerField(model_attr='score')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Playlist.objects.filter()

site.register(Bookmark, BookmarkIndex)
site.register(Playlist, PlaylistIndex)
