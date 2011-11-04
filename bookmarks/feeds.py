from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
import django.shortcuts as shortcuts
from models import Bookmark, Playlist
from django.contrib.auth.models import User
from tagging.models import Tag, TaggedItem

DEFAULT_LIMIT = 20
BOOKMARK_TITLE_TEMPLATE = 'feeds/bookmark_title.html'
BOOKMARK_DESCRIPTION_TEMPLATE = 'feeds/bookmark_description.html'

class LatestBookmarksFeed(Feed):
    """ All bookmarks ordered by -created, number returned limited by DEFAULT_LIMIT """    
    
    title_template = BOOKMARK_TITLE_TEMPLATE 
    description_template = BOOKMARK_DESCRIPTION_TEMPLATE
    
    title = "FavOERites latest bookmarks"
    description = "Latest bookmark additions FavOERites"
    link = '/browse/bookmarks/'
    
    def items(self):
        return Bookmark.objects.order_by('-created')[:DEFAULT_LIMIT]
    
class TopBookmarksFeed(Feed):
    """ Unique bookmarks ordered by score, number returned limited by DEFAULT_LIMIT
    
        As query is not a QuerySet item_link _title and _description are defined
    """
    
    title = "FavOERites top bookmarks"
    description = "Top scoring bookmarks on FavOERites"
    link = '/browse/bookmarks/'
    
    def items(self):
        return Bookmark.objects.get_unique_by_score()[:DEFAULT_LIMIT]
    
    def item_link(self, item):
        return reverse('bookmarks.bookmark_views.view', args=(item['user__username'], item['slug']))
    
    def item_title(self, item):
        return item['title']
    
    def item_description(self, item):
        return "Score: %s" % item['score']
        
class UserLatestBookmarksFeed(Feed):
    """ All bookmarks for given username, ordered by -created, number returned limited by DEFAULT_LIMIT """   
    
    title_template = BOOKMARK_TITLE_TEMPLATE 
    description_template = BOOKMARK_DESCRIPTION_TEMPLATE 
        
    def title(self, obj):
        return "%s's latest bookmarks" % (obj)
    
    def description(self, obj):
        return "Latest bookmarks from FavOERites user %s" % (obj)

    def link(self, obj):
        return reverse('bookmarks.bookmark_views.index', kwargs={'username':obj.username})
    
    def get_object(self, request, username):
        return shortcuts.get_object_or_404(User, username=username)
    
    def items(self, obj):
        return Bookmark.objects.get_by_user(obj.id).order_by('-created')[:DEFAULT_LIMIT]
    
class UserTopBookmarksFeed(Feed):
    """ All bookmarks for given username, ordered by -score, number returned limited by DEFAULT_LIMIT """
    
    def title(self, obj):
        return "%s's top bookmarks" % (obj)
    
    def description(self, obj):
        return "Top scoring bookmarks from FavOERites user %s" % (obj)

    def link(self, obj):
        return reverse('bookmarks.bookmark_views.index', kwargs={'username':obj.username})
    
    def get_object(self, request, username):
        return shortcuts.get_object_or_404(User, username=username)
    
    def items(self, obj):
        return Bookmark.objects.get_unique_by_score(obj.id)[:DEFAULT_LIMIT]
    
    def item_link(self, item):
        return reverse('bookmarks.bookmark_views.view', args=(item['user__username'], item['slug']))
    
    def item_title(self, item):
        return item['title']
    
    def item_description(self, item):
        return "Score: %s" % item['score']


class PlaylistBookmarksFeed(Feed):
    """ All bookmarks for given playlist slug, not limited"""
    
    title_template = BOOKMARK_TITLE_TEMPLATE 
    description_template = BOOKMARK_DESCRIPTION_TEMPLATE 
        
    def title(self, obj):
        return "'%s' playlist" % (obj.title)
    
    def description(self, obj):
        return "Bookmark from %s's playlist - %s" % (obj.user, obj)

    def link(self, obj):
        return reverse('bookmarks.playlist_views.view', kwargs={'username':obj.user,'slug':obj.slug})
    
    def get_object(self, request, slug):
        return shortcuts.get_object_or_404(Playlist, slug=slug)
    
    def items(self, obj):
        return Bookmark.objects.filter(playlist=obj) # no limit show all

class PlaylistTopScoreFeed(Feed):
    """ All bookmarks for given playlist slug, ordered by -score, number returned limited by DEFAULT_LIMIT """
    
    title = "FavOERites top playlists"
    description = "Top scoring playlists on FavOERites"
    link = '/browse/playlists/'
        
    def items(self):
        return Playlist.objects.get_by_score()[:DEFAULT_LIMIT]
    
    def item_link(self, item):
        return reverse('bookmarks.playlist_views.view', args=(item.user.username, item.slug))
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return "Score: %s" % item.score

class PlaylistTopFollowersScoreFeed(Feed):
    """ All bookmarks for given playlist slug, ordered by number of followers, number returned limited by DEFAULT_LIMIT """

    title = "FavOERites top playlists - by number of followers"
    description = "Playlists on FavOERites with the most followers"
    link = '/browse/playlists/'
        
    def items(self):
        return Playlist.objects.get_by_followers()[:DEFAULT_LIMIT]
    
    def item_link(self, item):
        return reverse('bookmarks.playlist_views.view', args=(item.user.username, item.slug))
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return "Followed by - %s" % item.num
    
class TagLatestBookmarksFeed(Feed):
    """ All bookmarks tagged with tag, number returned limited by DEFAULT_LIMIT """
    
    title_template = BOOKMARK_TITLE_TEMPLATE 
    description_template = BOOKMARK_DESCRIPTION_TEMPLATE 
        
    def title(self, obj):
        return "%s latest bookmarks" % (obj)
    
    def description(self, obj):
        return "Latest bookmarks from FavOERites tag %s" % (obj)

    def link(self, obj):
        return reverse('bookmarks.views.tags', kwargs={'tag':obj.name})
    
    def get_object(self, request, tag):
        return shortcuts.get_object_or_404(Tag, name=tag)
    
    def items(self, obj):
        return TaggedItem.objects.get_by_model(Bookmark,obj)[:DEFAULT_LIMIT]
    