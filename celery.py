import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luvira.settings')
app = Celery('luvira')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()