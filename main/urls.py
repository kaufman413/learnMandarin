from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lesson/(?P<number>[0-9]+)$', views.lesson, name='lesson'),
    url(r'^lesson/(?P<number>[0-9]+)/questions$', views.questions, name='questions'),
    url(r'logoff$', views.logoff, name='logoff'),
    url(r'ajaxPractice/(?P<username>[A-Za-z]+)/(?P<amount>[0-9]+)$', views.ajaxPractice, name='ajaxPractice'),
]