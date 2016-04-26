from django.conf.urls import url

from django_statsd import views


urlpatterns = [
    url('^record$', views.record, name='django_statsd.record'),
]
