from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^registration', views.registration, name='registration'),
    url(r'^registerUser', views.registerUser, name='registerUser'),
    url(r'^loginUser', views.loginUser, name='loginUser'),
]