from django.conf.urls import url
from user import views

urlpatterns = [
    url(r'^login', views.login),
    url(r'^signup', views.signup),
    url(r'^logout', views.logout),
    url(r'^details', views.details),
]
