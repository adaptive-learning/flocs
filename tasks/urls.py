"""Practice API URL Configuration
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from tasks import views

urlpatterns = [
    url(r'^get-ids/$', views.get_all_tasks),
    url(r'^get-task/(?P<id>[0-9]+)$', views.get_task_by_id),
]
