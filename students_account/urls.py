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
    (r'^students/(?P<group_name>(\w+))$', 'view_students'),
    (r'^students/delete/(?P<student_pk>(\d+))$', 'delete_student'),
    (r'^groups/delete/(?P<group_pk>(\d+))$', 'delete_group'),
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
