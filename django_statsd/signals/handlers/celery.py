from __future__ import absolute_import

import time
from django_statsd.clients import statsd
from celery import signals

_task_start_times = {}


def on_task_publish(sender=None, **kwargs):
    """
    Handle Celery ``task_sent`` signals.
    """
    # Increase statsd counter.
    statsd.incr('celery.%s.sent' % sender)


def on_task_prerun(sender=None, task_id=None, task=None, **kwds):
    """
    Handle Celery ``task_prerun``signals.
    """
    # Increase statsd counter.
    statsd.incr('celery.%s.start' % task.name)

    # Keep track of start times. (For logging the duration in the postrun.)
    _task_start_times[task_id] = time.time()


def on_task_postrun(sender=None, task_id=None, task=None, **kwds):
    """
    Handle Celery ``task_postrun`` signals.
    """
    # Increase statsd counter.
    statsd.incr('celery.%s.done' % task.name)

    # Log duration.
    start_time = _task_start_times.pop(task_id, False)
    if start_time:
        ms = int((time.time() - start_time) * 1000)
        statsd.timing('celery.%s.runtime' % task.name, ms)


def on_task_failure(sender=None, task_id=None, task=None, **kwds):
    """
    Handle Celery ``task_failure`` signals.
    """
    # Increase statsd counter.
    statsd.incr('celery.%s.failure' % task)


signals.after_task_publish.connect(on_task_publish)
signals.task_prerun.connect(on_task_prerun)
signals.task_postrun.connect(on_task_postrun)
signals.task_failure.connect(on_task_failure)
