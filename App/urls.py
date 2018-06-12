from django.conf.urls import url

urlpatterns = [
	url(r'Microtask5/', views.get_article_view_count, name='get_article_view_count'),
]
