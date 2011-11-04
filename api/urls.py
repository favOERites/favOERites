from django.conf.urls.defaults import *
from resources import  *
from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(CommentResource())
v1_api.register(UserProfileResource())
v1_api.register(UserResource())
v1_api.register(BookmarkResource())
v1_api.register(UserBookmarkResource())
v1_api.register(PlaylistResource())
v1_api.register(PlaylistBookmarksResource())
v1_api.register(VoteResource())

urlpatterns = patterns('',
    (r'^', include(v1_api.urls)),
)