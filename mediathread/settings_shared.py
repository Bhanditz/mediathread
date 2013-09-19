# Django settings for mediathread project.

# if you add a 'deploy_specific' directory
# then you can put a settings.py file and templates/ overrides there
# (see bottom)

from courseaffils import policies
from django.contrib.messages import constants as message_constants
import os
import re
import sys

APP_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)))
PROJECT_ROOT = os.path.join(APP_ROOT, '..')

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('admin', 'mediathread@example.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['.ccnmtl.columbia.edu', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mediathread',
        'HOST': '',
        'PORT': '',
        'USER': '',
        'PASSWORD': '',
    }
}

if 'test' in sys.argv or 'jenkins' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
        }
    }

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)

PROJECT_APPS = ['mediathread.main',
                'mediathread.djangosherd',
                'mediathread.assetmgr',
                'mediathread.projects',
                'mediathread.reports',
                'mediathread.discussions']

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    ('--cover-package=mediathread.main,mediathread.djangosherd,'
     'mediathread.assetmgr,mediathread.projects,mediathread.user_accounts,mediathread.course'),
]

CACHE_BACKEND = 'locmem:///'

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False

MEDIA_ROOT = "uploads/"
MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'collected_static')
STATIC_URL = '/site_media/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'media'),
)

#appends a slash if nothing is found without a slash.
APPEND_SLASH = True

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

# ## be careful: if you add/remove something here
# ## do the same with settings_production.py
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'mediathread.main.views.django_settings',
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

MIDDLEWARE_CLASSES = (
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'courseaffils.middleware.CourseManagerMiddleware',
    'mediathread.main.middleware.AuthRequirementMiddleware',
    'mediathread.course.middleware.CallToActionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

ROOT_URLCONF = 'mediathread.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # Put application templates before these fallback ones:
    #"/var/www/mediathread/templates/",
    #os.path.join(os.path.dirname(__file__), "deploy_specific/templates"),
    os.path.join(os.path.dirname(__file__), "templates"),
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.flatpages',
    'django.contrib.messages',
    'django.contrib.markup',
    'sorl.thumbnail',
    'courseaffils',
    'django.contrib.sites',
    'django.contrib.admin',
    'tagging',
    'smartif',
    'modelversions',
    'structuredcollaboration',
    'mediathread.djangosherd',
    'mediathread.assetmgr',
    'mediathread.projects',
    'mediathread.discussions',
    'django.contrib.comments',
    'threadedcomments',
    'djangohelpers',
    'mediathread.reports',
    'mediathread.main',
    'south',
    'django_nose',
    'compressor',
    'django_jenkins',
    'mediathread.taxonomy',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'mediathread.user_accounts',
    'autocomplete_light',
    'mediathread.course',
    'crispy_forms',
    'storages',
    'collectfast',
    'avatar',
]

COMPRESS_PARSER = "compressor.parser.HtmlParser"
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_CSS_FILTERS = [
    'mediathread.s3_utils.CustomCssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
    'compressor.filters.template.TemplateFilter'
]

THUMBNAIL_SUBDIR = "thumbs"
EMAIL_SUBJECT_PREFIX = "[mediathread] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "mediathread@example.com"
PUBLIC_CONTACT_EMAIL = "mediathread@example.com"

# External url for issue reporting system or e-mail notification
CONTACT_US_DESTINATION = ""

DATE_FORMAT = DATETIME_FORMAT = "g:i a, m/d/y"
LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL = '/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'django',
    },
    'johnny': {
        'BACKEND': 'johnny.backends.locmem.LocMemCache',
        'LOCATION': 'johnny',
        'JOHNNY_CACHE': True,
    }
}
CACHE_MIDDLEWARE_KEY_PREFIX = 'django'
JOHNNY_MIDDLEWARE_KEY_PREFIX = 'johnny'


# for AuthRequirementMiddleware. this should be a list of
# url prefixes for paths that can be accessed by anonymous
# users. we need to allow anonymous access to the login
# page, and to static resources.

ANONYMOUS_PATHS = ('/course/create/',
                   '/user_accounts/'
                   '/site_media/',
                   '/accounts/',
                   '/admin/',
                   '/api/',
                   '/help/',
                   '/course/join-sample-course/'
                   )

NON_ANONYMOUS_PATHS = ('/user_accounts/invite_students/',
                       '/course/',
                       '/asset/',
                       '/annotations/',
                       '/contact/',
                       '/yourspace/',
                       '/project/',
                       '/explore/',
                       '/comments/',
                       '/reports/',
                       '/discussion/',
                       '/archive/',
                       '/assignment/',
                       '/dashboard/',
                       '/_main/',
                       '/analysis/',
                       '/taxonomy/',
                       re.compile(r'^/$'),
                       )

# save is an exception, for server2server api
COURSEAFFILS_PATHS = NON_ANONYMOUS_PATHS + ('/save', '/settings')

COURSEAFFILS_EXEMPT_PATHS = ANONYMOUS_PATHS
COURSEAFFIL_AUTO_MAP_GROUPS = ['demo']

COMMENTS_ALLOW_PROFANITIES = True
COMMENTS_APP = 'threadedcomments'
COMMENT_MAX_LENGTH = None

FORCE_LOWERCASE_TAGS = True

# if you set this to a string, then bookmarklet can import from flickr
DJANGOSHERD_FLICKR_APIKEY = None
FLOWPLAYER_SWF_LOCATION = \
    "https://releases.flowplayer.org/swf/flowplayer-3.2.16.swf"

DEFAULT_COLLABORATION_POLICY = policies.InstructorManaged()

# django-allauth settings
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 14
ACCOUNT_USER_DISPLAY = 'mediathread.user_accounts.utils.display_user'


# Customer.io keys
CUSTOMERIO_SITE_ID = ''
CUSTOMERIO_API_KEY = ''

# Mailchimp arguments
MAILCHIMP_API_KEY = ''
MAILCHIMP_REGISTRATION_LIST_ID = ''

# Segment.io key
SEGMENTIO_API_KEY = ''
SEGMENTIO_JS_KEY = ''

# The sample course that all registered users are added to
SAMPLE_COURSE_ID = 2

CRISPY_TEMPLATE_PACK = 'bootstrap'

# Don't show info messages from allauth
MESSAGE_LEVEL = message_constants.SUCCESS

# URLs that appear in the header and footer
ABOUT_URL = "http://www.getmediathread.com/"
HELP_URL = "http://support.appsembler.com/knowledgebase/topics/39118-mediathread"


# this gets around Django 1.2's stupidity for commenting
# we're already checking that the request is from someone in the class
def no_reject(request, reason):
    request.csrf_processing_done = True
    return None

CSRF_FAILURE_VIEW = no_reject

# if you add a 'deploy_specific' directory
# then you can put a settings.py file and templates/ overrides there
try:
    from mediathread.deploy_specific.settings import *
    if 'EXTRA_INSTALLED_APPS' in locals():
        INSTALLED_APPS = INSTALLED_APPS + EXTRA_INSTALLED_APPS
    if 'EXTRA_MIDDLEWARE_CLASSES' in locals():
        MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + EXTRA_MIDDLEWARE_CLASSES
except ImportError:
    pass
