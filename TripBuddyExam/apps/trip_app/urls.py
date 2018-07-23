from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),
    url(r'createUser$', views.createUser),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^travels$', views.travel),
    url(r'^addtrip$', views.addTrip),
    url(r'^createTrip$', views.createTrip),
    url(r'^view/(?P<description_id>\d+)$', views.view),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^cancel/(?P<id>\d+)$', views.cancel),
]