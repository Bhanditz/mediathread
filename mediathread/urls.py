from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from djangosherd.api import SherdNoteResource
from mediathread.api import TagResource
from mediathread.assetmgr.api import AssetResource
from mediathread.main.api import CourseResource, CourseSummaryResource
from mediathread.projects.api import ProjectResource
from mediathread.taxonomy.api import TermResource, VocabularyResource
from tastypie.api import Api
import os.path


v1_api = Api(api_name='v1')
v1_api.register(SherdNoteResource())
v1_api.register(AssetResource())
v1_api.register(ProjectResource())
v1_api.register(CourseResource())
v1_api.register(CourseSummaryResource())
v1_api.register(TermResource())
v1_api.register(VocabularyResource())
v1_api.register(TagResource())


admin.autodiscover()

bookmarklet_root = os.path.join(os.path.dirname(__file__),
                                "../media/",
                                "bookmarklets")

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)

auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))
logout_page = (r'^accounts/logout/$',
               'django.contrib.auth.views.logout',
               {'next_page': redirect_after_logout})

if hasattr(settings, 'WIND_BASE'):
    auth_urls = (r'^accounts/', include('djangowind.urls'))
    logout_page = (r'^accounts/logout/$', 'djangowind.views.logout',
                   {'next_page': redirect_after_logout})


urlpatterns = patterns(
    '',

    (r'^crossdomain.xml$', 'django.views.static.serve',
     {'document_root': os.path.abspath(os.path.dirname(__file__)),
      'path': 'crossdomain.xml'}),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root':
      os.path.abspath(os.path.join(os.path.dirname(admin.__file__), 'media')),
      'show_indexes': True}),

    (r'^comments/', include('django.contrib.comments.urls')),

    logout_page,

    auth_urls,  # see above

    (r'^contact/', login_required(
        TemplateView.as_view(template_name="main/contact.html"))),

    (r'^stats/', TemplateView.as_view(template_name="stats.html")),

    (r'^smoketest/', include('smoketest.urls')),

    (r'^admin/', admin.site.urls),

    (r'^jsi18n', 'django.views.i18n.javascript_catalog'),

    # Bookmarklet + cache defeating
    url(r'^bookmarklets/(?P<path>analyze.js)$', 'django.views.static.serve',
        {'document_root': bookmarklet_root}, name='analyze-bookmarklet'),
    url(r'^nocache/\w+/bookmarklets/(?P<path>analyze.js)$',
        'django.views.static.serve', {'document_root': bookmarklet_root},
        name='nocache-analyze-bookmarklet'),

    # Courseafills
    url(r'^accounts/logged_in.js$', 'courseaffils.views.is_logged_in',
        name='is_logged_in.js'),
    url(r'^nocache/\w+/accounts/logged_in.js$',
        'courseaffils.views.is_logged_in', name='nocache-is_logged_in.js'),
    url(r'^api/user/courses$', 'courseaffils.views.course_list_query',
        name='api-user-courses'),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),

    # Homepage
    (r'^$', 'mediathread.main.views.triple_homepage'),
    (r'^yourspace/', include('mediathread.main.urls')),
    (r'^_main/api/', include(v1_api.urls)),

    # Instructor Dashboard & reporting
    (r'^reports/', include('mediathread.reports.urls')),

    url(r'^dashboard/migrate/',
        'mediathread.main.views.migrate',
        name="dashboard-migrate"),
    url(r'^dashboard/sources/',
        'mediathread.main.views.class_manage_sources',
        name="class-manage-sources"),
    url(r'^dashboard/settings/',
        'mediathread.main.views.class_settings',
        name="class-settings"),

    url(r'^taxonomy/', include('mediathread.taxonomy.urls')),

    # Collections Space
    (r'^asset/', include('mediathread.assetmgr.urls')),
    (r'^annotations/', include('mediathread.djangosherd.urls')),

    # Bookmarklet Entry point
    # Staff custom asset entry
    url(r'^save/$',
        'mediathread.assetmgr.views.asset_create',
        name="asset-save"),

    # Composition Space
    (r'^project/', include('mediathread.projects.urls')),

    # Discussion
    (r'^discussion/', include('mediathread.discussions.urls')),

    # Manage Sources
    url(r'^explore/redirect/$',
        'mediathread.assetmgr.views.source_redirect',
        name="source_redirect"),

    ### Public Access ###
    (r'', include('structuredcollaboration.urls')),
)
