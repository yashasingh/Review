from django.conf.urls import url

from . import views

app_name='App'
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^Microtask1/', views.main, name = 'main'),
    url(r'^Microtask2/', views.main2, name = 'main2'),
]