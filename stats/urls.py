"""Statistics API URL Configuration
"""

from django.conf.urls import include, url
from stats import views

urlpatterns = [
    url(r'^student-statistics$', views.get_student_statistics),
]
