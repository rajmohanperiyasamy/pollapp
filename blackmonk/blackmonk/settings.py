# Django settings for blackmonk project.
from ConfigParser import RawConfigParser
import os

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

project_path = lambda a: os.path.join(PROJECT_PATH, a)
here = lambda a: os.path.join(os.path.abspath(os.path.dirname(__file__)), a)
config = RawConfigParser()
config.read(os.path.join(here(''), 'config.cfg'))

DEBUG = True
#DEBUG = False
COMPRESS_ENABLED=True
COMPRESS_DEBUG_TOGGLE = None
COMPRESS_ROOT=project_path('static/')
TEMPLATE_DEBUG = DEBUG

AUTH_USER_MODEL = 'usermgmt.BmUser'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

LOGIN_REDIRECT_URL = "/"

MANAGERS = ADMINS
MAINTENANCE_MODE=False
DATABASES = {
    'default': {
        'ENGINE': config.get('db_pgsql', 'ENGINE'), # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': config.get('db_pgsql', 'NAME'),                    # Or path to database file if using sqlite3.
        'USER': config.get('db_pgsql', 'USER'),                     # Not used with sqlite3.
        'PASSWORD': config.get('db_pgsql', 'PASSWORD'),              # Not used with sqlite3.
        'HOST': config.get('db_pgsql', 'HOST'),                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': config.get('db_pgsql', 'PORT'),                        # Set to empty string for default. Not used with sqlite3.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Calcutta'
#EMAIL_BACKEND = 'seacucumber.backend.SESBackend'
EMAIL_BACKEND = 'common.backends.BmSmtpEmailBackend'

AUTH_PROFILE_MODULE = 'usermgmt.BmUser'

AUTHENTICATION_BACKENDS = ('common.backends.EmailAuthBackend','django.contrib.auth.backends.ModelBackend')

# Language code for this installation. All choices can be found project_path:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = project_path('media/')
MEDIA_TOUR_ROOT = project_path('templates/')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/site_media/'
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    project_path('static/'),
)
GEOIP_PATH=project_path('static/geoip/GeoLiteCity.dat')
LOCALE_PATHS = (
     project_path('locale/'),
   
)
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'wnnru8vbj^te=)+$yhhl0y_*x_2r1!+xg_$k@l^8_qp8x)vy3x'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
# AUTHENTICATION_BACKENDS = ('common.backends.EmailAuthBackend',)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'openid_login.middleware.OpenIDMiddleware',
    'common.middleware.SiteLogin',

    'common.middleware.ThemeTemplate',
    'common.validatebrowser.ValidateBrowser',
    #'common.checkapps.CheckApps',
    
    
    #'common.createSession.CreateSessionMiddleware',

)

TEMPLATE_CONTEXT_PROCESSORS = (
                                                             
    "django.contrib.auth.context_processors.auth",
    'django.core.context_processors.request',
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    #'django.core.context_processors.csrf',
    #"common.context_processors.getsettings",
     "common.context_processors.getsettings",
     #"common.context_processors.weather",
)
ROOT_URLCONF = 'blackmonk.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'blackmonk.wsgi.application'

LOGIN_URL='/account/signin/'

LOGIN_REDIRECT_URL='/' #/accounts/overview/

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    project_path('templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    'django.contrib.markup',
    'easy_thumbnails',
    'photo_library',
    'usermgmt',
    'common',

    #'compressor',
    
    'locality',
    'events',
    'deal',
    'videos',
    'classifieds',
    'article',
    'community',
    #'forum',
    'business',
    'movies',
    'gallery',
    'polls',
    'banners',
    'payments',
    #'payments.paypal.standard.pdt',
    'payments.paypal.standard.ipn',
    'payments.googlecheckout',
    'payments.authorizenet',
    'payments.stripes',
    'attraction',
    #'seacucumber',
    'storages',
    'channels',
    #'south',
    'meetup',
    'buzz',
    #'advice',
    #'djcelery',
    #'restaurants',
    'hotels',
    'flowers',
    'jobs',
    'bookmarks',
    'sweepstakes',
    'bmshop.shop',
    'bmshop.products',
    'bmshop.cart',
    'bmshop.customer',
    'bmshop.order',
    'django_countries',
  
  'haystack',
  'twitter_login',
  'openid_login',
  'fbconnect',
  'news',
  'linkedin',
  
  'analytics',
  'mptt',
  'mptt_comments',
  'django.contrib.sitemaps',
  'djcelery',
  'kombu.transport.django',
  'celery_haystack',
  'compressor',
)
BROKER_URL = 'django://'
import djcelery
djcelery.setup_loader()
HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'
HAYSTACK_DEFAULT_OPERATOR = 'OR'

#EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
#DATABASE_ROUTERS = ['common.db_routers.CeleryRouter',]
FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
   
)
FILE_UPLOAD_TEMP_DIR = project_path('media/')

DEFAULT_FROM_EMAIL = config.get('email', 'DEFAULT_FROM_EMAIL')
DEFAULT_INFO_EMAIL = config.get('email', 'DEFAULT_INFO_EMAIL')

    
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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

from log_settings import *
from app_settings import *
from prod_settings import *
PAYPAL_DEBUG=True
OPENID_CREATE_USERS=True
HAYSTACK_CONNECTIONS = {'default': {'ENGINE': 'haystack.backends.xapian_backend.XapianEngine','PATH': project_path('xapian_index/localengine.com'), },}
LIVE=True
TEMPLATE_THEME_PATH="default/"

#CELERY_TIMEZONE = 'UTC'

INTERNAL_IPS = ('192.168.1.24',)
ALLOWED_HOSTS = ['demo.blackmonk.com']
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION':config.get('common', 'CACHE'),
    }
}
