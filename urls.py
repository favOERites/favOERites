from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
import settings
import oerbookmarking.bookmarks.feeds as feeds

admin.autodiscover()

# FEEDS
urlpatterns = patterns('',
    url(r'^feed/bookmark/latest/$', feeds.LatestBookmarksFeed(), name='latest-bookmarks'),
    url(r'^feed/bookmark/top/$', feeds.TopBookmarksFeed(), name='top-bookmarks'),
    url(r'^feed/user/(?P<username>.*)/latest/$', feeds.UserLatestBookmarksFeed(), name='latest-user-bookmarks'),
    url(r'^feed/user/(?P<username>.*)/top/$', feeds.UserTopBookmarksFeed(), name='top-user-bookmarks'),
    url(r'^feed/playlist/followers/$', feeds.PlaylistTopFollowersScoreFeed(), name='playlist-followers'),
    url(r'^feed/playlist/top/$', feeds.PlaylistTopScoreFeed(), name='playlist-top'),
    url(r'^feed/playlist/(?P<slug>.*)/all/$', feeds.PlaylistBookmarksFeed(), name='playlist-bookmarks'),
    url(r'^feed/tag/(?P<tag>.*)/latest/$', feeds.TagLatestBookmarksFeed(), name='latest-tag'),
)

urlpatterns += patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('oerbookmarking.socialauth.urls')),
    #url(r'^accounts/', include('oerbookmarking.socialauth.urls')),
    url(r'^api/', include('oerbookmarking.api.urls')),
    url(r'^search/', include('oerbookmarking.haystack_urls')),
    url(r'^comments/post/$', 'oerbookmarking.bookmarks.views.comment_posted'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^', include('oerbookmarking.bookmarks.urls')),
    (r'^ajax_select/', include('ajax_select.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns("",
                            url(r'media/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),                           
            )