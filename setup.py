import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup( 
      name="django-gevent-socketio",
      version="0.1",
      packages=["django_gevent_socketio"],
      include_package_data=True,
      license="BSD License",
      description="Encapsulate gevent socketio into a reusable django app",
      long_description=README,
      url="http://github.com/bharling/django-gevent-socketio",
      author="Ben Harling",
      author_email="benjamin.harling@hotmail.com",
      install_requires=("gevent-socketio",),
      classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: SocketIO',
    ],
      
)