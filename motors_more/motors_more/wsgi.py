
"""
WSGI config for motors_more project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import socketio

from django.core.wsgi import get_wsgi_application
from django.conf import settings

from auction.schedule import print_something
import schedule
import threading
import time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'motors_more.settings')


def run_scheduled_job():
    schedule.every(1).seconds.do(print_something)

    while True:
        # print('22222222222222')
        schedule.run_pending()
        time.sleep(5)


# Start the scheduled job in a separate thread
job_thread = threading.Thread(target=run_scheduled_job)
job_thread.daemon = True
job_thread.start()

application = get_wsgi_application()
application = socketio.WSGIApp(settings.SIO, application)
