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
from practice import urls as practice_urls
from user import urls as user_urls
from tasks import urls as tasks_urls

urlpatterns = [
    # admin
    url(r'^admin/', include(admin.site.urls)),

    # server APiI
    url(r'^api/user/',include(user_urls)),
    url(r'^api/practice/', include(practice_urls)),
    url(r'^api/tasks/', include(tasks_urls)),
    url(r'^api/.*$', 'flocs.views.wrong_api_call'),

    # all other requests are resolved by the frontend app
    #url('^.*$', TemplateView.as_view(template_name='index.html')),
    url('^.*$', 'flocs.views.frontend_app'),
]
