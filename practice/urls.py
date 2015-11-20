"""Practice API URL Configuration
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from practice import views

urlpatterns = [
    url(r'^next-task$', views.get_next_task),
    url(r'^attempt-report$', views.post_attempt_report),
]
