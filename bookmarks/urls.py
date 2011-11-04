from django.conf.urls.defaults import *

urlpatterns = patterns('bookmarks.views',
    (r'^$', "index"),
    (r'^tag/(?P<tag>.*)/$', "tags"),
    (r'^test/$', "test"),
    (r'^close_iframe/$', "close_iframe"),
    (r'^bookmarks/$', "tags"),
    
    (r'^lookup/authors/add/$', "add_author"),
    (r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    
)

urlpatterns += patterns('bookmarks.browse_views',
    (r'^browse/$', "index"),
    (r'^browse/users/$', "users"),
    (r'^browse/bookmarks/$', "bookmarks"),
    (r'^browse/playlists/$', "playlists"),
)

urlpatterns += patterns('bookmarks.bookmark_views',
    (r'add_bookmark/$', "add_bookmark"),
    (r'(?P<username>.*)/bookmark/$', "index"),
    (r'(?P<username>.*)/bookmark/add/$', "add"),
    (r'(?P<username>.*)/bookmark/(?P<slug>.*)/edit/$', "edit"),
    (r'(?P<username>.*)/bookmark/(?P<slug>.*)/$', "view"),
)


urlpatterns += patterns('bookmarks.playlist_views',
    (r'add_to_playlist/$', "add_to_playlist"),
    (r'^(?P<username>.*)/playlist/$', "index"),
    (r'^(?P<username>.*)/playlist/add/$', "add"),
    (r'^(?P<username>.*)/playlist/(?P<slug>.*)/edit/$', "edit"),
    (r'^(?P<username>.*)/playlist/(?P<slug>.*)/unfollow/$', "unfollow"),
    (r'^(?P<username>.*)/playlist/(?P<slug>.*)/follow/$', "follow"),
    (r'^(?P<username>.*)/playlist/(?P<slug>.*)/fork/$', "fork"),
    (r'^(?P<username>.*)/playlist/(?P<slug>.*)/$', "view"),
)

urlpatterns += patterns('bookmarks.vote_views',
    (r'^vote/(?P<vote>.*)/(?P<object_id>.*)/(?P<content_type_id>.*)/$', "vote"),
)




