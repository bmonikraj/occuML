from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'index/', views.index, name='index'),
    url(r'result/', views.result, name='result'),
    url(r'mlearn/', views.m_learn, name='m_learn'),
    url(r'mongo/', views.mongoConn, name='mongoConn'),
]
