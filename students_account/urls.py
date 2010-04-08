import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('students_app.views',
    # Example:
    (r'^index/$', 'login'),
    (r'^logout/$', 'logout'),
    (r'^groups/$', 'view_groups'),
    (r'^groups/(?P<group_name>(\w*))$', 'view_students'),
    (r'^students/$', 'view_students'),
    (r'^edit/group/$', 'edit_group'),
    (r'^edit/student/$', 'edit_student'),
    (r'^jqgrid/(?P<grid_name>(\w+))/$', 'grid_handler', {}, 'grid_handler'),
    (r'^jqgrid/cfg/(?P<grid_name>(\w+))/$', 'grid_config', {}, 'grid_config'),
    # (r'^students_account/', include('students_account.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    { 'document_root': settings.MEDIA_ROOT }),
)
