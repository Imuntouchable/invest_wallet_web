from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'investment_portfolio.settings'
)
app = Celery('investment_portfolio')
app.conf.update(
    worker_pool='solo',
)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
