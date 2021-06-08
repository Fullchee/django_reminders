from django.urls import path
from . import views

urlpatterns = [
    path('', views.ping),
    path('links', views.get_all_links),
    path('random-link', views.get_random_link),
    path('keywords', views.get_keywords),
    path('link/<int:link_id>', views.get_link),
    path('search', views.search),
    path('add_link', views.add_link),
    path('update_link', views.update_link),
]