from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from social_auth import __version__ as version
from social_auth.backends import BACKENDS, OpenIdAuth, BaseOAuth, BaseOAuth2

def login(request):
    """Displays login links"""
    if request.user.is_authenticated():
        return HttpResponseRedirect('/auth/user/')
    else:
        backends = grouped_backends()
        allowed_names = ('facebook','google','twitter','yahoo')
        return render_to_response('home.html',
                                  {'backends': backends,
                                   'allowed_names': allowed_names},
                                  RequestContext(request))


def login_small(request):
    """Displays login links"""
    backends = grouped_backends()
    allowed_names = ('facebook','google','twitter','yahoo')
    return render_to_response('home_small.html',
                              {'backends': backends,
                               'allowed_names': allowed_names},
                              RequestContext(request))


@login_required
def loggedin(request):
    """Login complete view, displays user data"""
    allowed_names = ('facebook','google','twitter','yahoo')
    ctx = {'accounts': request.user.social_auth.all(),
           'version': version,
           'last_login': request.session.get('social_auth_last_login_backend'),
           'backends': grouped_backends(),
           'allowed_names': allowed_names}
    return render_to_response('account.html', 
                              ctx, 
                              RequestContext(request))

def error(request):
    """Error view"""
    error_msg = request.session.pop(settings.SOCIAL_AUTH_ERROR_KEY, None)
    return render_to_response('error.html', 
                              {'version': version,'error_msg': error_msg},
                              RequestContext(request))

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')


def grouped_backends():
    """Group backends by type"""
    backends = {'oauth': [],
                'oauth2': [],
                'openid': []}

    for name, backend in BACKENDS.iteritems():
        if issubclass(backend, BaseOAuth2):
            key = 'oauth2'
        elif issubclass(backend, BaseOAuth):
            key = 'oauth'
        elif issubclass(backend, OpenIdAuth):
            key = 'openid'
        else:
            print name, backend
        backends[key].append((name, backend))
    return backends