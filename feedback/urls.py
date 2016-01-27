"""
Feedback API URLs configuration
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add$', views.add_feedback_message),
]
