## Django settings for ASKBOT enabled project.
import os.path
import logging
import askbot
import site
import sys
from jinja2.runtime import Undefined
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

#this line is added so that we can import pre-packaged askbot dependencies
ASKBOT_ROOT = os.path.abspath(os.path.dirname(askbot.__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
site.addsitedir(os.path.join(ASKBOT_ROOT, 'deps'))

DEBUG = False   # set to True to enable debugging
TEMPLATE_DEBUG = False  # keep false when debugging jinja2 templates
INTERNAL_IPS = ('127.0.0.1',)
ALLOWED_HOSTS  = ['*',] #change this for better security on your site

ADMINS = (
    ('admin', 'admin@sovereignty.network'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',
        'PORT': '',
        'TEST': {
            'CHARSET': 'utf8', # Setting the character set and collation to utf-8
        }
    }
}

#outgoing mail server settings
SERVER_EMAIL = 'admin@sovereignty.network'
DEFAULT_FROM_EMAIL = 'admin@sovereignty.network'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = ''
EMAIL_HOST = ''
EMAIL_PORT = ''
EMAIL_USE_TLS = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # django.core.mail.backends.smtp.EmailBackend'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

LANGUAGE_CODE = 'en'
LANGUAGES = (('en', 'English'),)
ASKBOT_LANGUAGE_MODE = 'single-lang' #'single-lang', 'url-lang', 'user-lang'

# Absolute path to the directory that holds uploaded media
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'upfiles')
MEDIA_URL = '/upfiles/' # url to uploaded media. This is expected to start with a /
STATIC_URL = '/m/'#this must be different from MEDIA_URL
USE_LOCAL_FONTS = False

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Make up some unique string, and don't share it with anybody.
SECRET_KEY = "4b71fe1641e4a36f435880a49a92f85420baaea3d0309e03479d11bd283632c5"

ASKBOT_COMMON_CONTEXT_PREPROCESSORS = [
    'askbot.context.application_settings',
    'askbot.user_messages.context_processors.user_messages',# must be before auth
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth', # this is required for the admin app
                                                   # not sure if the admin app even uses jinja2 ...
]

TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'APP_DIRS': True,
        'DIRS': [],
        'OPTIONS': {
            'environment': 'askbot.skins.jinja2_environment.factory',
            'autoescape': False,
            'undefined': Undefined,
            'context_processors': ASKBOT_COMMON_CONTEXT_PREPROCESSORS
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors':
                ['django.template.context_processors.request' ] # because DTL
                + ASKBOT_COMMON_CONTEXT_PREPROCESSORS
        }
    },
)

MIDDLEWARE = (
    'django.middleware.csrf.CsrfViewMiddleware',            # for csrf
    'django.contrib.sessions.middleware.SessionMiddleware', # prerequisite for user messages
    'django.contrib.messages.middleware.MessageMiddleware', # for user messages
    'django.middleware.common.CommonMiddleware',               # FIXME: why do we even have this?
    'django.contrib.auth.middleware.AuthenticationMiddleware', # FIXME: why do we even have this?

    'askbot.middleware.anon_user.ConnectToSessionMessagesMiddleware', # up next: get rid of this
    'askbot.middleware.forum_mode.ForumModeMiddleware',
    'askbot.middleware.cancel.CancelActionMiddleware',
    'askbot.middleware.view_log.ViewLogMiddleware',
    'askbot.middleware.spaceless.SpacelessMiddleware', # FIXME: why do we even have this?
)

ATOMIC_REQUESTS = True

ROOT_URLCONF = os.path.basename(os.path.dirname(__file__)) + '.urls'

#UPLOAD SETTINGS
FILE_UPLOAD_TEMP_DIR = os.path.join(
                                os.path.dirname(__file__),
                                'tmp'
                            ).replace('\\','/')

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)
ASKBOT_ALLOWED_UPLOAD_FILE_TYPES = ('.jpg', '.jpeg', '.gif', '.bmp', '.png', '.tiff')
ASKBOT_MAX_UPLOAD_FILE_SIZE = 1024 * 1024 #result in bytes
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


#TEMPLATE_DIRS = (,) #template have no effect in askbot, use the variable below
#ASKBOT_EXTRA_SKINS_DIR = #path to your private skin collection
#take a look here http://askbot.org/en/question/207/


INSTALLED_APPS = (
    'askbot',
    'askbot.deps.django_authopenid',
    'askbot.deps.group_messaging',

    ## part of django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    ## extra packages
    'avatar',
    'captcha',
    'compressor',
    'django_jinja',
    'django_countries',
    'followit',
    'keyedcache',
    'kombu.transport.memory',
    'livesettings',
    'robots',
    'tinymce',
)

#setup redis or memcached for production use!
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'askbot',
    }
}
# Chose a unique KEY_PREFIX to avoid clashes with other applications
# using the same cache (e.g. a shared memcache instance).
CACHES['default'].update({'KEY_PREFIX': 'askbot', 'TIMEOUT': 6000})
#sets a special timeout for livesettings if you want to make them different
LIVESETTINGS_CACHE_TIMEOUT = CACHES['default']['TIMEOUT']
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_SECONDS = 600

#If you use memcache you may want to uncomment the following line to enable memcached based sessions
#SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'askbot.deps.django_authopenid.backends.AuthBackend',
)

#logging settings
logging.basicConfig(
    filename=os.path.join(PROJECT_ROOT, 'log/askbot_app.log'),
    level=logging.CRITICAL,
    format='%(pathname)s TIME: %(asctime)s MSG: %(filename)s:%(funcName)s:%(lineno)d %(message)s',
)

###########################
#
#   this will allow running your forum with url like http://site.com/forum
#
#   ASKBOT_URL = 'forum/'
#
ASKBOT_URL = '' #no leading slash, default = '' empty string
ASKBOT_TRANSLATE_URL = True #translate specific URLs
_ = lambda v:v #fake translation function for the login url
LOGIN_URL = '/%s%s%s' % (ASKBOT_URL, _('account/'), _('signin/'))
LOGIN_REDIRECT_URL = ASKBOT_URL #adjust, if needed
#note - it is important that upload dir url is NOT translated!!!
#also, this url must not have the leading slash
ALLOW_UNICODE_SLUGS = False
ASKBOT_USE_STACKEXCHANGE_URLS = False #mimic url scheme of stackexchange

#Celery Settings
BROKER_TRANSPORT = "kombu.transport.memory.Transport"
CELERY_ALWAYS_EAGER = True

CSRF_COOKIE_NAME = '_csrf'

STATICFILES_DIRS = (
    ('default/media', os.path.join(ASKBOT_ROOT, 'media')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

NOCAPTCHA = True
ENABLE_HAYSTACK_SEARCH = False # don't enable it, will be removed

TINYMCE_COMPRESSOR = True
TINYMCE_SPELLCHECKER = False
TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, 'default/media/tinymce/')
TINYMCE_JS_URL = STATIC_URL + 'default/media/tinymce/tiny_mce.js'
TINYMCE_DEFAULT_CONFIG = {
    'convert_urls': False,
    'theme': 'advanced',
    'content_css': STATIC_URL + 'default/media/style/tinymce/content.css',
    'force_br_newlines': True,
    'force_p_newlines': False,
    'forced_root_block': '',
    'mode' : 'textareas',
    'oninit': 'TinyMCE.onInitHook',
    'plugins': 'askbot_imageuploader,askbot_attachment',
    'theme_advanced_toolbar_location' : 'top',
    'theme_advanced_toolbar_align': 'left',
    'theme_advanced_buttons1': 'bold,italic,underline,|,bullist,numlist,|,undo,redo,|,link,unlink,askbot_imageuploader,askbot_attachment',
    'theme_advanced_buttons2': '',
    'theme_advanced_buttons3' : '',
    'theme_advanced_path': False,
    'theme_advanced_resizing': True,
    'theme_advanced_resize_horizontal': False,
    'theme_advanced_statusbar_location': 'bottom',
    'editor_deselector': 'mceNoEditor',
    'width': '100%',
    'height': '250'
}

#delayed notifications, time in seconds, 15 mins by default
NOTIFICATION_DELAY_TIME = 60 * 15

GROUP_MESSAGING = {
    'BASE_URL_GETTER_FUNCTION': 'askbot.models.user_get_profile_url',
    'BASE_URL_PARAMS': {'section': 'messages', 'sort': 'inbox'}
}

ASKBOT_CSS_DEVEL = False
if 'ASKBOT_CSS_DEVEL' in locals() and ASKBOT_CSS_DEVEL == True:
    COMPRESS_PRECOMPILERS = (
        ('text/less', 'lessc {infile} {outfile}'),
    )

COMPRESS_JS_FILTERS = []
COMPRESS_PARSER = 'compressor.parser.HtmlParser'
JINJA2_EXTENSIONS = ('compressor.contrib.jinja2ext.CompressorExtension',)
JINJA2_TEMPLATES = ('captcha',) # FIXME: unused but checked in startup_procedures

VERIFIER_EXPIRE_DAYS = 3
AVATAR_AUTO_GENERATE_SIZES = (16, 32, 48, 128) #change if avatars are sized differently

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

None
