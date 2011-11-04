from django.contrib.auth.models import User
from django.conf.urls.defaults import url
from django.contrib.comments.models import Comment

from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import ReadOnlyAuthorization, Authorization
from tastypie.exceptions import NotFound

from bookmarks.forms import AddBookmark, AddPlaylist
from bookmarks.models import Bookmark, Playlist, Vote, UserProfile, PlaylistBookmarks
from utils import CustomFormValidation, PlaylistBookmarkValidation, VoteValidation, UserAuthorization, PlaylistBookmarUserAuthorization
from django.core.urlresolvers import reverse

from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType


ALL_STANDARD = ['exact','iexact','startswith', 'istartswith', 'contains','icontains', 'endswith', 'iendswith']

BASE_BOOKMARK_FILTERING = {"slug": ALL_STANDARD,
                           "title": ALL_STANDARD,
                           "url": ALL_STANDARD,
                           "keywords": ALL_STANDARD,
                           "authors": ALL_WITH_RELATIONS,
                           "licences": ALL_WITH_RELATIONS,
                           "publishers": ALL_WITH_RELATIONS,
                           "user": ALL_WITH_RELATIONS,
                           'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
                           'modified': ['exact', 'range', 'gt', 'gte', 'lt', 'lte']}

BASE_PLAYLIST_FILTERING = {"slug": ALL_STANDARD,
                           "title": ALL_STANDARD,
                           "followers": ALL_WITH_RELATIONS,
                           "user": ALL_WITH_RELATIONS,
                           'created': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
                           'modified': ['exact', 'range', 'gt', 'gte', 'lt', 'lte']}


BASE_BOOKMARK_ORDERING = ['slug', 'title', 'url','score']
## USER
class UserProfileResource(ModelResource):
    
    total_score = fields.CharField(attribute='total_score')
    bookmarks_score = fields.CharField(attribute='bookmarks_score')
    playlist_score = fields.CharField(attribute='playlist_score')
    
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'userprofile'
        allowed_methods = ['get']
        fields = ['user',]
        
    def override_urls(self):
        """ allow access by username rather then id """
        return [url(r"^(?P<resource_name>%s)/(?P<user__username>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail")]

    def _build_reverse_url(self, name, args=None, kwargs=None):
        """ As there now two instances of the URL 'api_dispatch_detail', we want to call the one with username, by default pk is used """ 
        pk = kwargs.pop('pk')
        object = self.obj_get(pk=pk)
        kwargs['user__username'] = object.user.username
        return reverse(name, args=args, kwargs=kwargs)
    
class UserResource(ModelResource):
    bookmarks = fields.ToManyField('oerbookmarking.api.resources.BookmarkResource', 'bookmarks', full=True)
    playlists = fields.ToManyField('oerbookmarking.api.resources.PlaylistResource', 'playlists', full=False)
    following_playlists = fields.ToManyField('oerbookmarking.api.resources.PlaylistResource', 'following_playlists', full=False)
    editor_playlists  = fields.ToManyField('oerbookmarking.api.resources.PlaylistResource', 'playlist_editor', full=False)
    
    user_meta = fields.ToManyField(UserProfileResource, 'profile', full=True)
    
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ['get']
        fields = ['username',]
        authentication = ApiKeyAuthentication()
        ordering = ['username',]
        filtering = {'username':['exact'], ## workaround, GET username clashed with ApiKeyAuthentication() - https://github.com/toastdriven/django-tastypie/issues/201
                     'following_playlists': ALL_WITH_RELATIONS,
                     'parent_fork': ALL_WITH_RELATIONS,
                     'bookmarks': ALL_WITH_RELATIONS,
                     }

    def build_filters(self, filters=None):
        """ As username clashes with username in Auth, pop from filters, otherwise it will also be applied """
        filters.pop('username')
        return super(UserResource, self).build_filters(filters)

    def override_urls(self):
        """ allow access by username rather then id """
        return [url(r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail")]

    def _build_reverse_url(self, name, args=None, kwargs=None):
        """ As there now two instances of the URL 'api_dispatch_detail', we want to call the one with username, by default pk is used """
        if name ==  'api_dispatch_detail':
            pk = kwargs.pop('pk')
            object = self.obj_get(pk=pk)
            kwargs['username'] = object.username
            return reverse(name, args=args, kwargs=kwargs)


## COMMENTS 

class CommentResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    object = fields.ForeignKey('oerbookmarking.api.resources.BookmarkResource', 'content_object', null=True)
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
        allowed_methods = ['get', 'post', 'delete'] ## no update on comments?  
        authentication = ApiKeyAuthentication()
        authorization = UserAuthorization()
        filtering = {'comment': ALL_STANDARD,}
        fields = ['comment', 'user', 'submit_date']

    def obj_create(self, bundle, request=None, **kwargs):
        """ assign authorized user to comment    """
        return super(CommentResource, self).obj_create(bundle, request, user=request.user, site=Site.objects.get_current())
   
## BOOKMARKS

class BookmarkResource(ModelResource):
    # read only fields
    slug = fields.CharField(attribute='slug', readonly=True)
    created = fields.DateTimeField(attribute='created', readonly=True)
    modified = fields.DateTimeField(attribute='modified', readonly=True)   
    
    user = fields.ForeignKey(UserResource, 'user')
    score = fields.CharField(attribute='score')
    up_votes = fields.CharField(attribute='up')
    down_votes = fields.CharField(attribute='down')
    comments = fields.ToManyField(CommentResource, 'comments', full=True,  null=True)

    class Meta:
        queryset = Bookmark.objects.all()
        resource_name = 'bookmark'
        list_allowed_methods = ['get', 'post']
        authentication = ApiKeyAuthentication()
        authorization = UserAuthorization()
        filtering = BASE_BOOKMARK_FILTERING
        validation = CustomFormValidation(form_class=AddBookmark)
        fields = ['title', 'slug', 'url', 'description', 'keywords', 'created', 'modified']
        ordering = fields
    def is_valid(self, bundle, request=None):
        """ hook to pass request """
        return super(BookmarkResource, self).is_valid(bundle, request)
    
    def obj_create(self, bundle, request=None, **kwargs):
        """ assign authorized user to bookmark"""
        return super(BookmarkResource, self).obj_create(bundle, request, user=request.user)
    
class UserBookmarkResource(BookmarkResource):
    user = fields.ForeignKey(UserResource, 'user')
    score = fields.CharField(attribute='score')
    
    """ GET all bookmarks belonging to user """
    def __init__(self, *args, **kwargs):
        self._meta.limit = 1000
        self._meta.resource_name = 'mybookmarks'
        super(UserBookmarkResource, self).__init__(*args, **kwargs)
        
    def apply_authorization_limits(self, request, object_list):
        """ limit to authorized user """
        return object_list.filter(user=request.user)

## PLAYLIST

class PlaylistResource(ModelResource):
    # read only fields
    slug = fields.CharField(attribute='slug', readonly=True)
    created = fields.DateTimeField(attribute='created', readonly=True)
    modified = fields.DateTimeField(attribute='modified', readonly=True)
    
    # meda data
    user = fields.ForeignKey(UserResource, 'user')
    score = fields.CharField(attribute='score')
    up_votes = fields.CharField(attribute='up')
    down_votes = fields.CharField(attribute='down')
    bookmarks = fields.ToManyField('oerbookmarking.api.resources.BookmarkResource', 'bookmarks', null=True)
    comments = fields.ToManyField(CommentResource, 'comments', full=True,  null=True)
    
    class Meta:
        queryset = Playlist.objects.all()
        resource_name = 'playlist'
        allowed_methods = ['get', 'post'] # no edit or delete on playlist A
        authentication = ApiKeyAuthentication()
        authorization = UserAuthorization()
        filtering = BASE_PLAYLIST_FILTERING
        validation = CustomFormValidation(form_class=AddPlaylist)
        fields = ['title', 'slug', 'created', 'modified']
        ordering = fields
        
    def save_m2m(self, bundle):
        """ Tastypie does not support Through tables, so pop bookmarks and don't change"""
        
        self.fields.pop('bookmarks')
        bundle.data.pop('bookmarks')
        return super(PlaylistResource, self).save_m2m(bundle)

    def is_valid(self, bundle, request=None):
        """ hook to pass request """
        return super(PlaylistResource, self).is_valid(bundle, request)
    
    def obj_create(self, bundle, request=None, **kwargs):
        """ assign authorized user to playlist"""
        return super(PlaylistResource, self).obj_create(bundle, request, user=request.user)
    
## PLAYLIST BOOKMARK
class PlaylistBookmarksResource(ModelResource): 
    bookmark = fields.ForeignKey(BookmarkResource, 'bookmark')
    playlist = fields.ForeignKey(PlaylistResource, 'playlist') 
    class Meta:
        queryset = PlaylistBookmarks.objects.all()
        resource_name = 'playlistbookmarks'
        allowed_methods = ['get','post', 'put']#no delete on API yet, needs id.
        authentication = ApiKeyAuthentication()
        authorization = PlaylistBookmarUserAuthorization()
        validation = PlaylistBookmarkValidation()
        
    def is_authorized(self, request, object=None):
        """ For new object we need to check if user can add to this playlist, work around to tastypie issue """
        try:
            deserialized_data = self.deserialize(request, request.raw_post_data, format=request.META.get('CONTENT_TYPE', 'application/json'))
            playlist_obj = None
            playlist =  deserialized_data.get('playlist', None)
            if playlist:
                playlist_obj = PlaylistResource().get_via_uri(playlist)
        except:
            raise NotFound
        
        return super(PlaylistBookmarksResource, self).is_authorized(request, object=playlist_obj)

    def is_valid(self, bundle, request=None):
        obj = self.full_hydrate(bundle).obj
        bundle.data['bookmark'] = obj.bookmark
        bundle.data['playlist'] = obj.playlist
        return super(PlaylistBookmarksResource, self).is_valid(bundle, request)
 
class VoteResource(ModelResource): 
    object = fields.ForeignKey(BookmarkResource, 'voted_object', null=True)
    class Meta:
        queryset = Vote.objects.all()
        resource_name = 'vote'
        allowed_methods = ['get','post','put','delete']
        authentication = ApiKeyAuthentication()
        authorization = UserAuthorization()
        validation = VoteValidation()
        fields = ['value',]
        ordering = fields

    def is_valid(self, bundle, request=None):
        try:
            obj = self.full_hydrate(bundle).obj
            bundle.data['content_type'] = obj.content_type
            bundle.data['object_id'] = obj.object_id
        except:
            raise NotFound
    
            
        return super(VoteResource, self).is_valid(bundle, request)
    
    def obj_create(self, bundle, request=None, **kwargs):
        """ assign authorized user to playlist"""
        return super(VoteResource, self).obj_create(bundle, request, user=request.user)
    