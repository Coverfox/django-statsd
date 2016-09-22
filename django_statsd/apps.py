from django.apps import AppConfig
from django.conf import settings


class StatsdAppConfig(AppConfig):
    name = 'django_statsd'

    def ready(self):
        if getattr(settings, 'STATSD_MODEL_SIGNALS', False):
            from .signals.handlers import models  # NOQA

        if getattr(settings, 'STATSD_CELERY_SIGNALS', False):
            from .signals.handlers import celery  # NOQA
