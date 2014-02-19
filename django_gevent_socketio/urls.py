from django.conf.urls import patterns, include, url
import socketio.sdjango

socketio.sdjango.autodiscover()

urlpatterns = patterns("",
    url("^socket\.io", include(socketio.sdjango.urls)),
)