import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
          ('Your Name', 'yourname@example.com'),
    #('James Outterside', 'james@medev.ac.uk'),
    #('Paul Horner', 'paul.horner@ncl.ac.uk'),
    #('John Peterson', 'john.peterson@ncl.ac.uk'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'oerbookmarks',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True


PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")

MEDIA_URL = '/media/'

STATIC_ROOT = ''
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=u9rx5g=#vv3p9tj)221d7l&=8x&zvfv60k@#x(5lec#f6$1r2'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware'
)

ROOT_URLCONF = 'oerbookmarking.urls'

TEMPLATE_DIRS = (
    './templates/'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.media',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.humanize',
    'django.contrib.flatpages',
    'social_auth', #installed from https://github.com/omab/django-social-auth
    'socialauth', #local app using social_auth
    'bookmarks',
    'tagging',
    'tagging_autocomplete',
    'ajax_select',
    'haystack', 
    'tastypie',
    'extended_comments'
    #'debug_toolbar',
    
)

COMMENTS_APP = 'extended_comments'

#Your Authentication Backends - currently supports Google, Yahoo, Facebook, Twitter and OpenId
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.yahoo.YahooBackend',
    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

from django.template.defaultfilters import slugify
SOCIAL_AUTH_USERNAME_FIXER = lambda u: slugify(u)
SOCIAL_AUTH_UUID_LENGTH = 2

AUTH_PROFILE_MODULE = 'bookmarks.UserProfile'

# You'll need to sort these out too
TWITTER_CONSUMER_KEY         = ''
TWITTER_CONSUMER_SECRET      = ''
FACEBOOK_APP_ID              = ''
FACEBOOK_API_SECRET          = ''

LOGIN_REDIRECT_URL = '/auth/'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
'''
def custom_show_toolbar(request):
    return True # Always show toolbar, for example purposes only.


DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    'HIDE_DJANGO_SQL': False,
    'TAG': 'div',
}

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

'''
AJAX_LOOKUP_CHANNELS = {
    'author' : ('bookmarks.lookups', 'AuthorLookup'),
    'license' : ('bookmarks.lookups', 'LicenseLookup'),
    'non_staff_users' : ('bookmarks.lookups', 'UserLookup'),
    'bookmarks' : ('bookmarks.lookups', 'BookmarkLookup'),
}


HAYSTACK_SITECONF = 'oerbookmarking.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_ROOT, "whoosh_index") 

try:
    from local_settings import *
except:
    pass