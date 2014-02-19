=====
Django Gevent SocketIO
=====

A project to encapsulate the django example included in gevent-socketio into a resusable django application,
compatible with the latest version of django, and not using the bootstrap pattern, opting instead for
the traditional django application format.

Most of this code is ripped wholesale from socket.io and gevent-socketio, just packaged together by me.

Quick start
-----------

1. Add "django_gevent_socketio" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'django_gevent_socketio',
    )

2. Include the basic socketio URLconf in your project urls.py like this::

    url('', include('django_gevent_socketio.urls')),

3. Run the gevent development server with 
	
	./manage.py runserver_socketio