from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_statsd.clients import statsd


@receiver(post_save)
def model_save(sender, **kwargs):
    """
    Handle ``save`` events of all Django models.
    """
    instance = kwargs.get('instance')

    # Increase statsd counter.
    statsd.incr('models.%s.%s.%s' % (
        instance._meta.app_label,
        instance._meta.object_name,
        'create' if kwargs.get('created', False) else 'update',
    ))


@receiver(post_delete)
def model_delete(sender, **kwargs):
    """
    Handle ``delete`` events of all Django models.
    """
    instance = kwargs.get('instance')

    # Increase statsd counter.
    statsd.incr('models.%s.%s.delete' % (
        instance._meta.app_label,
        instance._meta.object_name,
    ))
