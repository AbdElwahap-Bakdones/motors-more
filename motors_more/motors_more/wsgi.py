"""
WSGI config for motors_more project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import socketio

from django.core.wsgi import get_wsgi_application
from auction.views import sio
from auction.schedule import run_cron_job
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motors_more.settings')


run_cron_job()

application = get_wsgi_application()
application = socketio.WSGIApp(sio, application)
