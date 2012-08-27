#!/usr/bin/env python26

# setup the virtualenv
import os
os.environ.setdefault('PATH', '/bin:/usr/bin')
os.environ['PATH'] = '/home/bellum/python/bin:' + os.environ['PATH']
os.environ['VIRTUAL_ENV'] = '/home/bellum/python/'
os.environ['PYTHON_EGG_CACHE'] = '/home/bellum/python/egg_cache'

os.chdir('/home/bellum/public_html/newbellum/main/')
import sys

# Add a custom Python path.
sys.path.insert(0, "/home/bellum/public_html/")
sys.path.insert(0, "/home/bellum/python/lib/python2.6/")
sys.path.insert(0, "/home/bellum/python/lib/python2.6/site-packages")

# Set the DJANGO_SETTINGS_MODULE environment variable  to the file in my
# application directory with the db settings etc.
# (filename minus the extension ".py")
os.environ['DJANGO_SETTINGS_MODULE'] = "main.settings"
from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
