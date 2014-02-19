from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djangosocketio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url('', include('django_gevent_socketio.urls')),
    url(r'^$', 'django_socketio_tests.views.home'),
    url(r'^admin/', include(admin.site.urls)),
)
