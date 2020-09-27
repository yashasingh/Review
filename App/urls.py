from django.conf.urls import url

from . import views

app_name='App'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^Microtask1/', views.get_recent_english_edits, name='get_recent_english_edits'),
    url(r'^Microtask2/', views.get_the_user_percentile, name='get_the_user_percentile'),
]
