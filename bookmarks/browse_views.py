import django.http as http
import django.shortcuts as shortcuts
import django.template.context as context
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from models import Bookmark, Playlist, User
from django.db.models import Sum, Count, Max, Avg

def index(request):
    bag = {}
    return shortcuts.render_to_response("browse/index.html", 
                                        bag, 
                                        context_instance=context.RequestContext(request))
    
def users(request):
    bag = {}
    users = User.objects.filter(is_active=True)
    users_by_bookmarks = Bookmark.objects.values('user__username').annotate(bookmarks=Count('user'), score=Sum('votes__value')).order_by('-score')

    bag['users'] = users_by_bookmarks
    return shortcuts.render_to_response("browse/users.html", 
                                        bag, 
                                        context_instance=context.RequestContext(request))
    
def bookmarks(request):
    bag = {}
    unique_bookmarks = Bookmark.objects.get_unique_by_score()
    bag['unique_bookmarks'] = unique_bookmarks
    return shortcuts.render_to_response("browse/bookmarks.html", 
                                        bag, 
                                        context_instance=context.RequestContext(request))
    
def playlists(request):
    bag = {}
    playlists = Playlist.objects.get_by_score()
    bag['playlists'] = playlists
    return shortcuts.render_to_response("browse/playlists.html", 
                                        bag, 
                                        context_instance=context.RequestContext(request))