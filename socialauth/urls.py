from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

    url(r'^$', 'socialauth.views.login', name='login'),
    url(r'^login-popup/$', 'socialauth.views.login_small', name='login_small'),
    url(r'^user/$', 'socialauth.views.loggedin', name='loggedin'),
    url(r'^login-error/$', 'socialauth.views.error', name='error'),
    url(r'^logout/$', 'socialauth.views.logout', name='logout'),
    
    url(r'', include('social_auth.urls')),
)
