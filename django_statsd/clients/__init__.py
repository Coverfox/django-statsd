import threading

from importlib import import_module
from django.utils.functional import SimpleLazyObject
from django.conf import settings


def get(name, default):
    try:
        return getattr(settings, name, default)
    except ImportError:
        return default


def get_client():
    local = threading.local()
    if not getattr(local, 'statsd_client', None):
        client = get('STATSD_CLIENT', 'statsd.client')
        host = get('STATSD_HOST', 'localhost')
        # This is causing problems with statsd
        # gaierror ([Errno -9] Address family for hostname not supported)
        # TODO: figure out what to do here.
        # host = socket.gethostbyaddr(host)[2][0]
        port = get('STATSD_PORT', 8125)
        prefix = get('STATSD_PREFIX', None)
        local.statsd_client = import_module(client).StatsClient(
            host=host, port=port, prefix=prefix
        )
    return local.statsd_client

statsd = SimpleLazyObject(get_client)
