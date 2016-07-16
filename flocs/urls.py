"""Flocs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from feedback import urls as feedback_urls
from practice import urls as practice_urls
from stats import urls as stats_urls
from tasks import urls as tasks_urls
from user import urls as user_urls
from social.apps.django_app import urls as social_urls

urlpatterns = [
    # admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS

    # server API
    url(r'^api/tasks/', include(tasks_urls)),
    url(r'^api/user/', include(user_urls)),
    url(r'^api/feedback/', include(feedback_urls)),
    url(r'^api/practice/', include(practice_urls)),
    url(r'^api/stats/', include(stats_urls)),
    url(r'^api/.*$', 'flocs.views.wrong_api_call'),

    # OAuth related urls
    url(r'^social/', include(social_urls, namespace='social')),

    # all other requests are resolved by the frontend app
    url('^.*$', 'flocs.views.frontend_app'),
]
