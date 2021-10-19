import os
from celery import Celery
from django.conf import settings


# set the default Django settings module for the 'celery' program.
if settings.DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tshop.settings.base')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tshop.settings.pro')

app = Celery('tshop')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
