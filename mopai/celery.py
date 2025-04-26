from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mopAi.settings')

app = Celery('mopAi')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = 'redis://redis:6379/0'
app.conf.result_backend = 'redis://redis:6379/0'

app.autodiscover_tasks()
